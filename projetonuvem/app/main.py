import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from scrap import randomadvice
import jwt
from datetime import datetime, timedelta

# Carregar variáveis de ambiente
load_dotenv()

# Obter as variáveis de ambiente
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_HOST = os.getenv("DATABASE_HOST")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# Construir a URL de conexão para o banco de dados PostgreSQL
DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"

# Criar engine de conexão
engine = create_engine(DATABASE_URL)

# Definir base do SQLAlchemy
Base = declarative_base()

# Criar sessão do SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Definir o modelo de usuário
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    senha = Column(String)

# Criação do banco de dados, se não existir
Base.metadata.create_all(bind=engine)

# Criação do FastAPI app
app = FastAPI()

# Configuração para o gerenciamento de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para verificar e gerar a senha
def verify_password(plain_password, senha):
    return pwd_context.verify(plain_password, senha)

def get_password_hash(password):
    return pwd_context.hash(password)

# Função para gerar o JWT
def create_access_token(data: dict):
    to_encode = data.copy()
    iat = datetime.utcnow()
    to_encode.update({"iat": iat})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependência para pegar a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependência para verificar o token JWT e retornar o usuário
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()), db: Session = Depends(get_db)):
    token = credentials.credentials
    if token is None:
        raise HTTPException(status_code=403, detail="Token não fornecido")
    
    try:
        # Decodifica o token JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Verifica o claim "sub"
        sub = payload.get("sub")
        if sub is None:
            raise HTTPException(status_code=403, detail="Token inválido (sub ausente)")
        # Busca o usuário no banco de dados
        user = db.query(User).filter(User.id == int(sub)).first()
        if user is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.PyJWTError:
        raise HTTPException(status_code=403, detail="Token inválido")
    
    return user

# Rota de registro
@app.post("/register")
def register(nome: str, email: str, senha: str, db: Session = Depends(get_db)):
    # Verificar se o email já existe
    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    # Criptografar a senha
    senha_hash = get_password_hash(senha)
    
    # Criar um novo usuário
    new_user = User(nome=nome, email=email, senha=senha_hash)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Gerar o token JWT
    access_token = create_access_token(data={"sub": str(new_user.id), "name":new_user.nome})
    return {"jwt": access_token}

# Rota de login
@app.post("/login")
def login(email: str, senha: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    
    if not user or not verify_password(senha, user.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    # Gerar o token JWT
    access_token = create_access_token(data={"sub": str(user.id), "name":user.nome})
    return {"jwt": access_token}

# Rota para consultar uma foto de pato (requisição autenticada com JWT)
@app.get("/consultar")
async def consultar(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Aqui você pode acessar a informação do usuário autenticado
    advice = randomadvice()
    return {"message": f"Bem-vindo, {current_user.nome}, aqui está um conselho para você: {advice}"}