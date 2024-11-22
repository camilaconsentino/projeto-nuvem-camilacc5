# ENTREGA 1
## *DOCKERIZING*

Camila Cardia Consentino

### explicação do projeto - scrap do que foi feito
Neste projeto, o usuário, uma vez tendo realizado seu registro e/ou login, poderá consultar uma API que retorna um conselho aleatório, em formato de texto

## explicação de como executar a aplicação
1. Rode no terminal:
`cd app` - para entrar na pasta
`docker compose up` - para rodar o conteiner

2. Abra o link API docs
`API docs: http://0.0.0.0:8000/docs`

3. No navegador, será necessário trocar '0.0.0.0' por 'localhost' no link, para entrar na interface da FastApi

4. Para realizar registro ou login, clique na barra correspondente à ação que voce quer realizar e depois clique em `Try Out`. Preencha os campos e clique em `Execute`. 

5. Se tudo der certo, o retorno será o token JWT, copie o token retornado

6. Para consultar a API, clique no botão `Authorize` no canto direito superior. Cole o token copiado no campo disponivel e clique em `authorize`

7. Clique na barra de `GET` `\consultar`, clique em `Try Out` e então em `Execute`. Não é necessário preencher nenhum campo pois o token já foi autenticado. A resposta dessa consulta será uma mensagem

### documentação dos endpoints da API
POST \register

POST \login

GET \consultar 

### screenshot com os endpoints testados

### video de execução DOCKER
https://drive.google.com/file/d/14TfMft3D4hzPfacRbFCedyNofXXfilUa/view?usp=sharing

### link para o docker hub do projeto
https://hub.docker.com/r/camilaconsentino/projetonuvem-camilacc5

### video de execucao AWS
https://drive.google.com/file/d/15bpYgMK8EAmbWeQPMo-jv1ZERCGC6gDw/view?usp=sharing