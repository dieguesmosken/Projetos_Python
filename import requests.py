import requests
import json

def search_google(query):
    unique_links = set()
    query = 'https://www.googleapis.com/customsearch/v1?key=MINHACHAVEAPI&cx=YOUR_CX&q=' + query
    response = requests.get(query)
    data = json.loads(response.text)
    for item in data['items']:
        link = item['link']
        if link.startswith("https://expo.chikoroko.art/toy/location_based/") or link.startswith("https://chikoroko.art/toy/location_based/"):
            if link not in unique_links:
                unique_links.add(link)
                print(link)

search_google("https://expo.chikoroko.art/toy/location_based/")
search_google("https://chikoroko.art/toy/location_based/")

