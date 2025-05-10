import yt_dlp
import os

def download_audio(url, download_path, is_playlist=False):
    try:
        if not os.path.exists(download_path):
            os.makedirs(download_path)
            print(f"Diretório '{download_path}' criado com sucesso.")
        
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]',
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'noplaylist': not is_playlist,
            'quiet': False,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"\n🔗 Baixando: {url}")
            ydl.download([url])
        
        print(f"✅ Concluído: {url}")
        return None  # Nenhum erro

    except yt_dlp.utils.DownloadError as e:
        mensagem = str(e)
        if "Requested format is not available" in mensagem:
            return "Formato de áudio não disponível para este vídeo."
        elif "Video unavailable" in mensagem:
            return "Vídeo indisponível ou privado."
        elif "HTTP Error" in mensagem:
            return "Erro de conexão ou bloqueio do YouTube."
        elif "Signature extraction failed" in mensagem:
            return "Erro ao decodificar a assinatura do vídeo."
        else:
            return f"Erro inesperado: {mensagem}"
    except Exception as e:
        return f"Erro desconhecido: {e}"

def obter_links():
    print("\nComo deseja fornecer os links?")
    print("1. Inserir manualmente")
    print("2. Carregar de um arquivo .txt")
    escolha = input("Digite 1 ou 2: ").strip()

    links = []

    if escolha == '1':
        print("\nCole os links dos vídeos ou playlists do YouTube:")
        print("➤ Pode colar múltiplos links separados por vírgula ou linha.")
        print("Digite 'fim' para encerrar a entrada dos links.\n")

        while True:
            linha = input()
            if linha.strip().lower() == 'fim':
                break
            elif ',' in linha:
                links.extend([link.strip() for link in linha.split(',') if link.strip()])
            elif linha.strip():
                links.append(linha.strip())
    
    elif escolha == '2':
        caminho_arquivo = input("Digite o caminho do arquivo .txt com os links: ").strip()
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                links = [linha.strip() for linha in arquivo if linha.strip()]
            print(f"{len(links)} link(s) carregados do arquivo.")
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
    else:
        print("Opção inválida! Nenhum link carregado.")

    return links

def main():
    print("=== Download de Áudios do YouTube ===")

    links = obter_links()

    if not links:
        print("Nenhum link fornecido. Encerrando.")
        return

    print("\nEscolha um diretório para salvar:")
    print("1. Usar o diretório padrão: 'C:/Users/kaio0/Downloads/atletica/'")
    print("2. Editar e escolher um diretório personalizado")
    option = input("Digite 1 ou 2: ").strip()

    if option == '1':
        download_path = 'C:/Users/kaio0/Downloads/atletica/'
    elif option == '2':
        download_path = input("Digite o diretório de destino: ").strip() or 'C:/Users/kaio0/Downloads/atletica/'
    else:
        print("Opção inválida! Usando o diretório padrão.")
        download_path = 'C:/Users/kaio0/Downloads/atletica/'

    print("\nEscolha o tipo de download:")
    print("1. Baixar áudio de vídeos individuais")
    print("2. Baixar áudio de playlists completas")
    download_type = input("Digite 1 ou 2: ").strip()
    is_playlist = download_type == '2'

    print(f"\n📥 Iniciando o download de {len(links)} link(s)...\n")

    erros = []

    for index, link in enumerate(links, start=1):
        print(f"\n🎵 ({index}/{len(links)}) Processando: {link}")
        erro = download_audio(link, download_path, is_playlist)
        if erro:
            erros.append((link, erro))
            print(f"❌ Falha: {erro}")

    if erros:
        print("\n⚠️ Alguns downloads falharam:")
        for link, motivo in erros:
            print(f"- {link} → {motivo}")
    else:
        print("\n✅ Todos os downloads foram concluídos com sucesso!")

if __name__ == "__main__":
    main()
