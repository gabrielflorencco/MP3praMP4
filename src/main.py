import os
import sys
import logging

from src.utils import create_output_folder, is_ffmpeg_available
from src.transcriber import transcribe_audio_to_srt
from src.video_editor import generate_video_with_subtitles

logging.basicConfig(level=logging.INFO)

def main(audio_path, image_path, traduzir):
    """
    Função principal que valida os caminhos de entrada, cria as pastas de saída e coordena o fluxo de
    transcrição e geração do vídeo com legendas.
    """
    if not os.path.exists(audio_path):
        logging.error(f"Arquivo de áudio não encontrado: {audio_path}")
        return
    if not os.path.exists(image_path):
        logging.error(f"Arquivo de imagem não encontrado: {image_path}")
        return
    if not is_ffmpeg_available():
        logging.error("FFmpeg não encontrado. Certifique-se de que está instalado e disponível no PATH do sistema.")
        return
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_base_path = os.path.join(script_dir, "outputs")
    os.makedirs(output_base_path, exist_ok=True)
    
    output_folder = create_output_folder(output_base_path, os.path.basename(audio_path))
    srt_path = transcribe_audio_to_srt(audio_path, traduzir)
    if srt_path is None:
        logging.error("Erro ao criar o arquivo SRT. O vídeo não será gerado.")
        return
    
    output_video_path = os.path.join(
        output_folder, 
        os.path.splitext(os.path.basename(audio_path))[0].replace(' ', '-') +
        ("_Traduzido" if traduzir else "") + ".mp4"
    )
    generate_video_with_subtitles(audio_path, srt_path, image_path, output_video_path)
    logging.info(f"Arquivo SRT salvo em: {srt_path}")
    logging.info(f"Arquivo de vídeo salvo em: {output_video_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python main.py <caminho_do_audio> <caminho_da_imagem> [-t]")
        sys.exit(1)
    
    input_audio = sys.argv[1]
    input_image = sys.argv[2]
    traduzir = "-t" in sys.argv
    
    main(input_audio, input_image, traduzir)