import os
import json
from mutagen.id3 import ID3
from datetime import datetime

music_directory = "music"

def find_music_files(directory):
    music_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.mp3') or file.endswith('.flac') or file.endswith('.wav') or file.endswith('.aac') or file.endswith('.m4a'):
                music_path = os.path.join(root, file)
                music_data = {
                    "name": file,
                    "path": music_path
                }
                try:
                    audio_data = ID3(music_path)
                    artist = audio_data["TPE1"].text[0]
                    music_data["artist"] = artist
                except:
                    music_data["artist"] = None
                music_files.append(music_data)
    return music_files

def extract_image(file_path, image_folder):
    music_data = {
            "name": os.path.basename(file_path),
            "artist": None,
            "image": None,
            "path": file_path
        }
    try:
        audio = ID3(file_path)
        for tag in audio.keys():
            if tag == 'APIC:':
                cover = audio[tag]
                image_file_name = os.path.basename(file_path).split(".")[0] + "." + cover.mime.split("/")[-1]
                if not os.path.exists(image_folder):
                    os.makedirs(image_folder)
                if not os.path.exists(os.path.join(image_folder, image_file_name)):
                    with open(os.path.join(image_folder, image_file_name), "wb") as img:
                        img.write(cover.data)
                        print(f"Imagem da música {os.path.basename(file_path)} salva em {os.path.join(image_folder, image_file_name)}")
                else:
                    print(f"Imagem da música {os.path.basename(file_path)} já existe em {os.path.join(image_folder, image_file_name)}")
                    music_data = {
                                    "name": os.path.basename(file_path),
                                    "artist": audio["TPE1"].text[0],
                                    "image": os.path.join(image_folder, image_file_name),
                                    "path": file_path
                                }
    except Exception as e:
        print(f"Não foi possível extrair informações da música {os.path.basename(file_path)}: {e}")
    return music_data

# exemplo de uso:
music_files = find_music_files(music_directory)
print("Buscando arquivos de música...")


# Salvando resultados em arquivo json
json_file_name = "resultados/json/music/musicas.json"
print("Salvando resultados em arquivo json...")
if not os.path.exists(json_file_name):
    with open(json_file_name, "w", encoding='utf-8') as json_file:
        json.dump(music_files, json_file, ensure_ascii=False)
        print("Resultados salvos com sucesso em ", json_file_name)
else:
    print("Arquivo ", json_file_name, " já existe, não foi sobreescrito")


# Salvando resultados em arquivo txt
txt_file_name = "resultados/txt/music/musicas.txt"
print("Salvando resultados em arquivo txt...")
if not os.path.exists(txt_file_name):
    with open(txt_file_name, "w", encoding='utf-8') as txt_file:
        for music_file in music_files:
            txt_file.write(f'{music_file["name"]} - {music_file["artist"]}\n')
    print("Resultados salvos com sucesso em ", txt_file_name)
else:
    print("Arquivo ", txt_file_name, " já existe, não foi sobreescrito")

