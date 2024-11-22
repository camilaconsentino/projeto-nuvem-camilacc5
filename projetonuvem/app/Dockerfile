# Use uma imagem base oficial do Python
FROM python:3.11-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app 

# Copia o arquivo requirements.txt para instalar as dependências
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos do projeto para o contêiner
COPY . .

EXPOSE 8000

# Define o comando de inicialização padrão para o contêiner
CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]