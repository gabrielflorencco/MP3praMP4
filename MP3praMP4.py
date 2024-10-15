import os
import sys
import whisper
import logging
import tempfile
import torch
from transformers import pipeline
from datasets import Dataset
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)

device = "cuda" if torch.cuda.is_available() else "cpu"
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-tc-big-en-pt", device=device)

def translate_batch(batch):
    """Traduz um lote de textos."""
    translations = translator(batch['text'], max_length=40)
    return {'translated_text': [translation['translation_text'] for translation in translations]}

def translate_texts(texts):
    """Cria um conjunto de dados e traduz os textos em paralelo."""
    dataset = Dataset.from_dict({'text': texts})
    translated_dataset = dataset.map(translate_batch, batched=True, batch_size=8)
    return translated_dataset['translated_text']

def transcribe_audio_to_srt(audio_file, traduzir=False):
    model = whisper.load_model("base", device=device)
    result = model.transcribe(audio_file, language='en')

    # Obtém o diretório do script e cria o caminho de saída
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "outputs", os.path.splitext(os.path.basename(audio_file))[0].replace(' ', '-'))
    os.makedirs(output_dir, exist_ok=True)

    srt_file_path = os.path.join(output_dir, "output.srt").replace('\\', '/')

    texts_to_save = [segment['text'].strip() for segment in result['segments']] if traduzir else []

    if traduzir and texts_to_save:
        # Traduzindo todos os textos em paralelo usando datasets
        translated_texts = translate_texts(texts_to_save)

    with open(srt_file_path, 'w', encoding='utf-8') as f:
        for index, segment in enumerate(result['segments'], start=1):
            start_time = int(segment['start'] * 1000)
            end_time = int(segment['end'] * 1000)
            text_to_save = translated_texts[index - 1] if traduzir and texts_to_save else segment['text'].strip()

            f.write(f"{index}\n")
            f.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
            f.write(f"{text_to_save}\n\n")

    return srt_file_path

def format_time(ms):
    hours = ms // 3600000
    minutes = (ms % 3600000) // 60000
    seconds = (ms % 60000) // 1000
    milliseconds = ms % 1000
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def generate_video_with_subtitles(audio_path, srt_path, image_path, output_video_path):
    video_temp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    video_temp.close()

    ffmpeg_cmd_temp = (
        f"ffmpeg -y -loop 1 -i \"{image_path}\" -i \"{audio_path}\" "
        f"-vf \"scale=894:880\" -c:v h264_nvenc -preset fast -b:v 5M "
        f"-c:a aac -b:a 192k -shortest \"{video_temp.name}\""
    )
    logging.info(f"Comando FFmpeg para vídeo temporário: {ffmpeg_cmd_temp}")

    os.system(ffmpeg_cmd_temp)

    ffmpeg_cmd_legenda = (
        f"ffmpeg -y -i \"{video_temp.name}\" -i \"{srt_path}\" "
        f"-c copy -c:s mov_text \"{output_video_path}\""
    )
    logging.info(f"Comando FFmpeg para adicionar legendas: {ffmpeg_cmd_legenda}")

    os.system(ffmpeg_cmd_legenda)
    os.remove(video_temp.name)
    logging.info(f"Vídeo temporário excluído: {video_temp.name}")

def create_output_folder(base_path, audio_filename):
    folder_name = os.path.splitext(audio_filename)[0].replace(' ', '-')
    output_folder = os.path.join(base_path, folder_name)

    counter = 1
    while os.path.exists(output_folder):
        output_folder = os.path.join(base_path, f"{folder_name}-{counter}")
        counter += 1

    os.makedirs(output_folder)
    return output_folder

def main(audio_path, image_path, traduzir):
    if not os.path.exists(audio_path):
        logging.error(f"Arquivo de áudio não encontrado: {audio_path}")
        return

    if not os.path.exists(image_path):
        logging.error(f"Arquivo de imagem não encontrado: {image_path}")
        return

    # Usar o diretório do script para armazenar os arquivos de saída
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_base_path = os.path.join(script_dir, "outputs")
    os.makedirs(output_base_path, exist_ok=True)

    output_folder = os.path.join(output_base_path, os.path.splitext(os.path.basename(audio_path))[0].replace(' ', '-'))
    os.makedirs(output_folder, exist_ok=True)
    
    srt_path = transcribe_audio_to_srt(audio_path, traduzir)
    if srt_path is None:
        logging.error("Erro ao criar o arquivo SRT. O vídeo não será gerado.")
        return

    output_video_path = os.path.join(output_folder, os.path.splitext(os.path.basename(audio_path))[0].replace(' ', '-') + ("_Traduzido" if traduzir else "") + ".mp4")
    generate_video_with_subtitles(audio_path, srt_path, image_path, output_video_path)

    logging.info(f"Arquivo SRT salvo em: {srt_path}")
    logging.info(f"Arquivo de vídeo salvo em: {output_video_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python script.py <caminho_do_audio> <caminho_da_imagem> [-t]")
        sys.exit(1)

    input_audio = sys.argv[1]
    input_image = sys.argv[2]
    traduzir = "-t" in sys.argv

    main(input_audio, input_image, traduzir)