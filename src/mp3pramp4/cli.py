import argparse
from mp3pramp4.main import main

def cli_entry():
    parser = argparse.ArgumentParser(description="Converte MP3 para MP4 com legendas.")

    parser.add_argument("audio_path", type=str, help="Caminho do arquivo de áudio (MP3/WAV).")
    parser.add_argument("image_path", type=str, help="Caminho da imagem de fundo.")
    parser.add_argument("-t", "--traduzir", action="store_true", help="Traduzir legenda para português.")

    args = parser.parse_args()

    main(args.audio_path, args.image_path, args.traduzir)
