import yt_dlp
import os
import shutil

def verificar_ffmpeg():
    """
    Verifica se o FFmpeg está disponível no sistema.
    """
    return shutil.which("ffmpeg") is not None and shutil.which("ffprobe") is not None

def escolher_diretorio():
    print("\nEscolha o diretório para salvar os arquivos:")
    caminho = input("Digite o caminho do diretório ou pressione Enter para usar o padrão ('~/Músicas/nova'): ").strip()

    if not caminho:
        caminho = os.path.expanduser("~/Músicas/nova")
    if not os.path.exists(caminho):
        os.makedirs(caminho)
        print(f"✅ Diretório '{caminho}' criado com sucesso.")
    return caminho

def download_audio(url, download_path, is_playlist=False):
    """
    Baixa apenas o áudio em formato m4a usando yt-dlp.
    """
    if not verificar_ffmpeg():
        print("❌ FFmpeg não encontrado. Por favor, instale e adicione ao PATH do sistema.")
        print("Tutorial: https://www.gyan.dev/ffmpeg/builds/")
        return

    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'noplaylist': not is_playlist,
        'quiet': False,
        'no_warnings': True,
        'merge_output_format': 'm4a',
        'ffmpeg_location': shutil.which("ffmpeg"),  # Caminho automático
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("\n🎧 Iniciando o download do áudio...\n")
            ydl.download([url])
        print(f"\n✅ Download concluído! Arquivo salvo em: {download_path}")
    except Exception as e:
        print(f"❌ Ocorreu um erro durante o download: {e}")
        print("ℹ️ Tentando listar os formatos disponíveis...\n")
        try:
            with yt_dlp.YoutubeDL({'quiet': False}) as ydl:
                ydl.download([f"--list-formats", url])
        except Exception as inner_e:
            print(f"❌ Falha ao listar os formatos: {inner_e}")

def main():
    print("=== Download de Áudios do YouTube ===")

    # Solicitar URL
    video_url = input("Digite a URL do vídeo ou playlist do YouTube: ").strip()
    if not video_url:
        print("❌ URL inválida. Encerrando.")
        return

    # Caminho para salvar
    download_path = escolher_diretorio()

    # Escolha de tipo de download
    print("\nEscolha o tipo de download:")
    print("1. Baixar o áudio de um único vídeo")
    print("2. Baixar o áudio de uma playlist completa")
    opcao = input("Digite 1 ou 2: ").strip()

    if opcao == '1':
        download_audio(video_url, download_path, is_playlist=False)
    elif opcao == '2':
        download_audio(video_url, download_path, is_playlist=True)
    else:
        print("❌ Opção inválida. Encerrando.")

if __name__ == "__main__":
    main()
