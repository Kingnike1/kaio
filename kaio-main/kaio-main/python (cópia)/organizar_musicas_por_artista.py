import os
import shutil
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen import MutagenError

def organize_music_by_artist(directory):
    """
    Organiza músicas em pastas baseadas no nome do artista (tag ID3).
    
    :param directory: Diretório contendo as músicas.
    """
    if not os.path.isdir(directory):
        print("❌ O caminho fornecido não é um diretório válido.")
        return

    # Criar uma pasta para músicas sem informações de artista
    unknown_artist_dir = os.path.join(directory, "Artista Desconhecido")
    if not os.path.exists(unknown_artist_dir):
        os.makedirs(unknown_artist_dir)

    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)

        # Ignorar subdiretórios ou arquivos que não sejam MP3
        if not os.path.isfile(file_path) or not file.lower().endswith('.mp3'):
            continue

        try:
            # Extrair informações de metadados usando Mutagen
            audio = MP3(file_path, ID3=EasyID3)
            artist = audio.get('artist', ['Artista Desconhecido'])[0].strip()

            # Criar a pasta do artista
            artist_dir = os.path.join(directory, artist)
            if not os.path.exists(artist_dir):
                os.makedirs(artist_dir)

            # Mover o arquivo para a pasta do artista
            shutil.move(file_path, os.path.join(artist_dir, file))
            print(f"✅ '{file}' movido para a pasta '{artist}'.")

        except MutagenError:
            # Mover arquivos sem metadados para a pasta de "Artista Desconhecido"
            shutil.move(file_path, os.path.join(unknown_artist_dir, file))
            print(f"⚠️ '{file}' movido para a pasta 'Artista Desconhecido' (sem metadados).")

    print("\n🎵 Organização concluída!")

def main():
    directory = input("Digite o caminho da pasta com as músicas sertanejas: ").strip()
    organize_music_by_artist(directory)

if __name__ == "__main__":
    main()
