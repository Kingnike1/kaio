import os
import glob
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor

def convert_to_mp3(input_file, output_file):
    """
    Converte um arquivo de áudio ou vídeo para MP3 usando o ffmpeg.
    
    :param input_file: Caminho do arquivo de entrada.
    :param output_file: Caminho do arquivo MP3 de saída.
    """
    try:
        command = [
            'ffmpeg', 
            '-i', input_file, 
            '-vn', 
            '-acodec', 'libmp3lame', 
            output_file
        ]
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        print(f"✅ Convertido: {input_file} -> {output_file}")
    except subprocess.CalledProcessError:
        print(f"❌ Falha ao converter: {input_file}")

def process_file(file_path, output_directory, converted_files):
    """
    Processa um único arquivo: converte ou move para o diretório de saída.
    
    :param file_path: Caminho do arquivo a ser processado.
    :param output_directory: Diretório de saída.
    :param converted_files: Lista de arquivos já processados.
    """
    file_name = os.path.basename(file_path)
    output_file = os.path.join(output_directory, os.path.splitext(file_name)[0] + ".mp3")
    
    if file_path.endswith(".mp3"):
        if output_file in converted_files:
            print(f"🔄 Arquivo já movido: {file_path}")
        else:
            shutil.move(file_path, output_file)
            print(f"📦 Movido: {file_path} -> {output_directory}")
    else:
        if output_file not in converted_files:
            convert_to_mp3(file_path, output_file)
        else:
            print(f"⏭️ Arquivo já convertido: {file_path}")

def batch_convert(directory, output_directory, file_types=("*.mp4", "*.m4a", "*.mp3")):
    """
    Converte ou move arquivos de áudio/vídeo para o formato MP3.
    
    :param directory: Diretório de entrada.
    :param output_directory: Diretório de saída.
    :param file_types: Tipos de arquivo a serem processados.
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Buscar arquivos no diretório
    files = []
    for file_type in file_types:
        files.extend(glob.glob(os.path.join(directory, file_type)))
    
    if not files:
        print("Nenhum arquivo para processar.")
        return

    # Identificar arquivos já convertidos
    converted_files = set(glob.glob(os.path.join(output_directory, "*.mp3")))

    # Processar arquivos com múltiplos threads
    with ThreadPoolExecutor() as executor:
        for file_path in files:
            executor.submit(process_file, file_path, output_directory, converted_files)

    print("\n✅ Processamento concluído.")

# Exemplo de uso
if __name__ == "__main__":
    input_directory = "/home/kingnike/Músicas/6"
    output_directory = "/home/kingnike/Músicas/mp3"
    
    if os.path.isdir(input_directory):
        batch_convert(input_directory, output_directory)
    else:
        print("❌ Diretório inválido. Verifique o caminho informado.")
