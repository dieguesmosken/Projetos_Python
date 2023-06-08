import os
import glob
from mutagen.mp3 import MP3
from mutagen.id3 import ID3

# diretório raiz
root = '../../music'

# lista todos os arquivos MP3 em todas as subpastas
mp3_files = list(glob.glob(root + '/**/*.mp3', recursive=True))

total_time = 0

# loop através dos arquivos
for file in mp3_files:
    try:
        # lê as informações do arquivo MP3
        audio = MP3(file)
        tags = ID3(file)

        # obtém a duração do arquivo
        duration = int(audio.info.length)
        total_time += duration

    except Exception as e:
        print(f"Não foi possível ler o arquivo {file}. Erro: {str(e)}")
        continue

# exibe o tempo total
print("Tempo total de todas as músicas:", total_time, "segundos")

