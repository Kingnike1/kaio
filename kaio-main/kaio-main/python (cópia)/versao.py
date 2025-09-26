import yt_dlp
from pathlib import Path

DEFAULT_DIR = Path.home() / "Músicas" / "nova"


def escolher_diretorio() -> Path:
    """Pergunta ao usuário o diretório para salvar os arquivos."""
    caminho = input(
        f"\n📂 Digite o caminho do diretório ou pressione Enter para usar o padrão ({DEFAULT_DIR}): "
    ).strip()

    diretorio = Path(caminho) if caminho else DEFAULT_DIR
    diretorio.mkdir(parents=True, exist_ok=True)  # cria se não existir
    print(f"✅ Usando diretório: {diretorio}")
    return diretorio


def download_audio(url: str, destino: Path, playlist: bool = False) -> None:
    """Baixa o melhor áudio disponível usando yt-dlp."""
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(destino / "%(title)s.%(ext)s"),
        "noplaylist": not playlist,
        "quiet": False,
        "no_warnings": True,
        "postprocessors": [],  # não usa ffmpeg
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("\n🎧 Iniciando o download...\n")
            ydl.download([url])
        print(f"\n✅ Download concluído! Arquivos em: {destino}")
    except Exception as e:
        print(f"❌ Erro durante o download: {e}")


def main():
    print("=== 🎵 Download de Áudios do YouTube (sem FFmpeg) ===")

    # URL do vídeo ou playlist
    url = input("🔗 Digite a URL do vídeo ou playlist: ").strip()
    if not url:
        return print("❌ URL inválida. Encerrando.")

    destino = escolher_diretorio()

    # Escolha de tipo de download
    opcoes = {"1": False, "2": True}
    escolha = input("\n1️⃣ Baixar um único vídeo\n2️⃣ Baixar playlist completa\nEscolha (1/2): ").strip()

    if escolha in opcoes:
        download_audio(url, destino, playlist=opcoes[escolha])
    else:
        print("❌ Opção inválida. Encerrando.")


if __name__ == "__main__":
    main()
# C:\Users\kaio0\Music\TA