import requests

# Define a URL base da API dos Correios
url = "https://api.tracktry.com/v1"

# Define o número de rastreamento
tracking_number = "NL546837377BR"

# Define os headers da requisição, incluindo o token de acesso
headers = {
    "Content-Type": "application/json",
    "Tracktry-Api-Key": "fc58bbde-adf3-4953-b812-f854dcabbf58"
}

# Define os parâmetros da requisição, incluindo o número de rastreamento
params = {
    "code": tracking_number,
    "lang": "pt-br"
}

# Envia a requisição para a API dos Correios
response = requests.get(f"{url}/trackings/get", headers=headers, params=params)

# Verifica se a resposta foi bem sucedida
if response.status_code == 200:
    # Extrai as informações de rastreamento da resposta JSON
    data = response.json()["data"]
    tracking_info = data["items"][0]["tracking"]

    # Itera sobre as atualizações de rastreamento e imprime na tela
    for update in tracking_info["events"]:
        print(update["checkpoint_time"], "-", update["checkpoint_status"])
else:
    print("Erro ao conectar à API dos Correios.")
