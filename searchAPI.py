import os, requests, json
api_key = "Sua key vai aqui"

def search_google(query):
    unique_links = set()
    start = 1
    while start <= 100:
        query = 'https://www.googleapis.com/customsearch/v1?key=SUA-APIKEY-VAI-AQUI&cx=SEU-CX-VAI-AQUI&q=' + query + '&start=' + str(start)
        response = requests.get(query)
        data = json.loads(response.text)
        if 'items' not in data:
            break
        for item in data['items']:
            link = item['link']
            if link.startswith("EXAMPLE TEXT") or link.startswith("ANOTHER EXAMPLE TEXT"):
                if link not in unique_links:
                    unique_links.add(link)
                    print(link)
        start += 10

    # criando pasta resultados/txt/
    if not os.path.exists("resultados/txt"):
        os.makedirs("resultados/txt")
    # escrevendo links unicos no arquivo de texto
    with open("resultados/txt/resultados.txt", "a+") as f:
        for link in unique_links:
            f.write(link + "\n")
    print("Resultados salvos com sucesso em resultados/txt/resultados.txt")

search_google("EXAMPLE")

# https://github.com/dieguesmosken/WebAppsHTML
