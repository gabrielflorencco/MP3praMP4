import os
import sys
import argparse
import logging

from mp3pramp4.utils import create_output_folder, is_ffmpeg_available
from mp3pramp4.transcriber import transcribe_audio_to_srt
from mp3pramp4.video_editor import generate_video_with_subtitles

logging.basicConfig(level=logging.INFO)

def main(audio_path, image_path, traduzir):
    """
    Função principal que valida os caminhos de entrada, cria as pastas de saída e coordena o fluxo de
    transcrição e geração do vídeo com legendas.
    """
    if not os.path.exists(audio_path):
        logging.error(f"Arquivo de áudio não encontrado: {audio_path}")
        sys.exit(1)
    
    if not os.path.exists(image_path):
        logging.error(f"Arquivo de imagem não encontrado: {image_path}")
        sys.exit(1)
    
    if not is_ffmpeg_available():
        logging.error("FFmpeg não encontrado. Certifique-se de que está instalado e disponível no PATH do sistema.")
        sys.exit(1)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_base_path = os.path.join(script_dir, "outputs")
    os.makedirs(output_base_path, exist_ok=True)
    
    output_folder = create_output_folder(output_base_path, os.path.basename(audio_path))
    srt_path = transcribe_audio_to_srt(audio_path, traduzir)
    
    if srt_path is None:
        logging.error("Erro ao criar o arquivo SRT. O vídeo não será gerado.")
        sys.exit(1)
    
    output_video_path = os.path.join(
        output_folder, 
        os.path.splitext(os.path.basename(audio_path))[0].replace(' ', '-') +
        ("_Traduzido" if traduzir else "") + ".mp4"
    )
    
    generate_video_with_subtitles(audio_path, srt_path, image_path, output_video_path)
    
    logging.info(f"Arquivo SRT salvo em: {srt_path}")
    logging.info(f"Arquivo de vídeo salvo em: {output_video_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Converte MP3 para MP4 com legendas.")

    parser.add_argument("audio_path", type=str, help="Caminho do arquivo de áudio (MP3/WAV).")
    parser.add_argument("image_path", type=str, help="Caminho da imagem de fundo.")
    parser.add_argument("-t", "--traduzir", action="store_true", help="Traduzir legenda para português.")

    args = parser.parse_args()

    # Aqui, estamos passando os parâmetros corretamente para o main()
    main(args.audio_path, args.image_path, args.traduzir)