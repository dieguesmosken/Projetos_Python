from pytube import YouTube
import os

# Configure o diretório onde os vídeos serão salvos
SAVE_DIR = "/downloadyt/"

# Obtenha o URL do canal do YouTube
channel_url = "https://youtube.com/@pudimpinho"

# Baixe todos os vídeos do canal
for video_url in YouTube.get_videos_from_channel(channel_url):
    try:
        # Crie uma instância do objeto YouTube
        yt = YouTube(video_url)

        # Obtenha o título do vídeo
        title = yt.title.replace("/", "-")

        # Configure o caminho de salvamento do vídeo
        save_path = os.path.join(SAVE_DIR, f"{title}.mp4")

        # Se o arquivo ainda não foi baixado, baixe-o
        if not os.path.exists(save_path):
            print(f"Baixando {title}...")
            stream = yt.streams.filter(file_extension="mp4", progressive=True).first()
            stream.download(output_path=SAVE_DIR)
        else:
            print(f"{title} já foi baixado.")
    except Exception as e:
        print(f"Não foi possível baixar o vídeo {video_url}: {e}")
