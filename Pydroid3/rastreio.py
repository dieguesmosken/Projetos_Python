import requests
from bs4 import BeautifulSoup

# Define a URL do site de rastreamento dos Correios
url = "https://www2.correios.com.br/sistemas/rastreamento/resultado_semcontent.cfm"

# Define os parâmetros da requisição (número de rastreamento)
params = {
    "objetos": "NL546837377BR"
}

# Envia a requisição para o site dos Correios
response = requests.get(url, params=params)

# Verifica se a resposta foi bem sucedida
if response.status_code == 200:
    # Faz o parsing do HTML com BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontra a tabela com as informações de rastreamento
    table = soup.find("table", {"class": "listEvent sro"})

    # Verifica se a tabela foi encontrada
    if table is not None:
        # Itera sobre as linhas da tabela para extrair as informações de rastreamento
        for row in table.find_all("tr"):
            date = row.find("td", {"class": "sroDtEvent"}).text.strip()
            location = row.find("td", {"class": "sroLbEvent"}).text.strip()
            status = row.find("td", {"class": "sroStEvent"}).text.strip()

            # Imprime as informações de rastreamento
            print(f"{date} - {location} - {status}")
    else:
        print("Tabela não encontrada.")
else:
    print("Erro ao conectar ao site dos Correios.")
