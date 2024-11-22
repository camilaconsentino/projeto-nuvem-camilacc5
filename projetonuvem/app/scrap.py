import requests

def randomadvice():
    # URL da API que retorna uma imagem de pato (pode ser GIF ou outra imagem)
    url = 'https://api.adviceslip.com/advice'

    # Realiza o request da página
    response = requests.get(url)

    # Verifica se o request foi bem-sucedido
    if response.status_code == 200:
        data = response.json()
        advice = data['slip']['advice']
        return advice
        
    else:
        print("Erro ao acessar a página.")
