import os
import logging
import tempfile

from src.utils import is_ffmpeg_available, run_command

def generate_video_with_subtitles(audio_path, srt_path, image_path, output_video_path):
    """
    Gera um vídeo utilizando uma imagem estática, adiciona o áudio e insere as legendas a partir do arquivo SRT.
    """
    if not is_ffmpeg_available():
        logging.error("FFmpeg não encontrado. Certifique-se de que está instalado e disponível no PATH do sistema.")
        return
    
    # arquivo temporário pro vídeo sem legendas
    video_temp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    video_temp.close()
    
    # gerando o vídeo
    ffmpeg_cmd_temp = (
        f"ffmpeg -y -loop 1 -i \"{image_path}\" -i \"{audio_path}\" "
        f"-vf \"scale=894:880\" -c:v h264_nvenc -preset fast -b:v 5M "
        f"-c:a aac -b:a 192k -shortest \"{video_temp.name}\""
    )
    logging.info(f"Comando FFmpeg para vídeo temporário: {ffmpeg_cmd_temp}")
    run_command(ffmpeg_cmd_temp)
    
    # incorporando as legendas no vídeo final
    ffmpeg_cmd_legenda = (
        f"ffmpeg -y -i \"{video_temp.name}\" -i \"{srt_path}\" "
        f"-c copy -c:s mov_text \"{output_video_path}\""
    )
    logging.info(f"Comando FFmpeg para adicionar legendas: {ffmpeg_cmd_legenda}")
    run_command(ffmpeg_cmd_legenda)
    
    # deleta o arquivo temporário
    os.remove(video_temp.name)
    logging.info(f"Vídeo temporário excluído: {video_temp.name}")
