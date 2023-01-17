import xml.etree.ElementTree as ET
import requests
import os

# Google Translate API key
api_key = 'AIzaSyAn43-htRSUgkX3DYafkFr8lknE5xjo924'

# Função de tradução
def traduzir_texto(text, source_lang, target_lang, api_key):
    url = f"https://translation.googleapis.com/language/translate/v2?key={api_key}&q={text}&source={source_lang}&target={target_lang}"
    response = requests.get(url)
    data = response.json()
    return data["data"]["translations"][0]["translatedText"]

# Caminhos de entrada e saída
#input_path = 'Traducao/English'
output_path = 'Traducao/Portugues'

# Pergunta ao usuario qual a pasta de entrada

input_path = input("Digite o caminho da pasta de entrada: ")

# Checar se a pasta de entrada existe
if not os.path.exists(input_path):
    # exibe a mensagem de erro
    print(f"O caminho {input_path} não existe.")
    exit()

# Criar pasta de saída se não existir
if not os.path.exists(output_path):
    os.makedirs(output_path)
    
        
# Traduzir todos os arquivos XML na pasta de entrada
for file_name in os.listdir(input_path):
    if file_name.endswith(".xml"):
        output_file = os.path.join(output_path, file_name)
        if os.path.exists(output_file):
            print(f"{file_name} foi traduzido anteriormente.")
            continue
        print(f"Processando arquivo: {file_name}")
        # Ler arquivo XML
        try:
            # lê o arquivo XML
            tree = ET.parse(os.path.join(input_path, file_name))
        except Exception as e:
            # exibe a mensagem de erro
            print(f"Erro lendo arquivo {file_name}")
            continue
        
        root = tree.getroot()

        # Traduzir valores
        for settings in root.findall(".//Settings"):
            key = settings.find("./key") or settings.find("./Key")
            # se a key não for nula e o texto não for nulo
            if key is not None and key.text is not None:
                 # define o valor da key value
                value = settings.find("./value") or settings.find("./Value")
                if value is not None and value.text is not None:
                    try:
                        # traduz o texto
                        translated_value = traduzir_texto(value.text, "en", "pt-BR", api_key)
                        #translated_value = traduzir_texto(unescape(value.text), "en", "pt-BR", api_key)
                        value.text = translated_value
                    except Exception as e:
                        # exibe a mensagem de erro
                        print(f"Erro durante a tradução de '{value.text}': {e}")
                        continue
                else:
                    # exibe a mensagem de erro
                    print(f"Valor não encontrado no arquivo {file_name}")
            else:
                # exibe a mensagem de erro
                print(f"Key não encontrado no arquivo {file_name}")

        # Salvar arquivo XML traduzido
        try:
            # salva o arquivo com codificação utf-8
            tree.write(os.path.join(output_path, file_name), encoding='utf-8')
            print("Tradução completa.")
        except Exception as e:
            # exibe a mensagem de erro
            print(f"Erro ao salvar arquivo: {e}")
