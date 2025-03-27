import os
import logging
import shutil
import subprocess
import tempfile

def is_ffmpeg_available():
    """Verifica se o FFmpeg está disponível no PATH."""
    return shutil.which("ffmpeg") is not None

def run_command(command):
    """Executa um comando no shell e trata possíveis erros."""
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro ao executar comando: {command}")
        logging.error(e)

def format_time(ms):
    """Formata milissegundos para o formato SRT (HH:MM:SS,mmm)."""
    hours = ms // 3600000
    minutes = (ms % 3600000) // 60000
    seconds = (ms % 60000) // 1000
    milliseconds = ms % 1000
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def create_output_folder(base_path, audio_filename):
    """Cria uma pasta de saída baseada no nome do arquivo de áudio."""
    folder_name = os.path.splitext(audio_filename)[0].replace(' ', '-')
    output_folder = os.path.join(base_path, folder_name)
    os.makedirs(output_folder, exist_ok=True)
    return output_folder