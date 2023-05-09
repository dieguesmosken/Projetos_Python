import requests
import os
import json

def search_google(filter_url):
    query = filter_url
    unique_links = set()
    start = 1
    while start <= 100:
    
        query = 'https://www.googleapis.com/customsearch/v1?key=AIzaSyCNheU4QFa_Y-C_4ZFBnylG9Upp--EZ6EA&cx=913dd1a9015d64921&q=' + query + '&start=' + str(start)
        response = requests.get(query)
        data = json.loads(response.text)
        if 'items' not in data:
            break
        for item in data['items']:
            link = item['link']
            if filter_url in link:
                if link not in unique_links:
                    if filter_word in item['snippet']:
                        unique_links.add(link)
                        print(link)
        start += 10

    # criando pasta resultados/txt/
    if not os.path.exists("resultados/txt"):
        os.makedirs("resultados/txt")
    # escrevendo links unicos no arquivo de texto
    with open("resultados/txt/resultados2.txt", "a+") as f:
        for link in unique_links:
            f.write(link + "\n")
    print("Resultados salvos com sucesso em resultados/txt/resultados2.txt")

filter_url = input("Insira a palavra a ser filtrado: ")
search_google(filter_url)
