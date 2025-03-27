import os
import logging
import torch
import whisper

from src.utils import create_output_folder, format_time
from src.translator import translate_texts

def transcribe_audio_to_srt(audio_file, traduzir=False):
    """
    Transcreve o áudio utilizando o Whisper e gera um arquivo SRT.
    
    Se 'traduzir' for True, os textos serão traduzidos para o português.
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model("base", device=device)
    result = model.transcribe(audio_file, language='en')
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = create_output_folder(os.path.join(script_dir, "outputs"), os.path.basename(audio_file))
    srt_file_path = os.path.join(output_dir, "output.srt").replace('\\', '/')
    
    # Obtém os textos originais para tradução, se necessário
    texts_to_save = [segment['text'].strip() for segment in result['segments']] if traduzir else []
    if traduzir and texts_to_save:
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