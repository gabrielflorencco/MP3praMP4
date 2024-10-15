# 🎵 MP3 para MP4 Converter 📼

Este é um script simples que transforma seus arquivos de áudio em vídeos com uma imagem de fundo estática e legendas em inglês ou português.

## 📋 Sumário

1. [Pré-requisitos](#pré-requisitos)
2. [Instalação](#instalação)
3. [Como Usar](#como-usar)
4. [Solução de Problemas](#solução-de-problemas)
5. [Contribuição](#contribuição)

## 🛠 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- Python 3.10 ou superior
- Git
- FFmpeg

## 🚀 Instalação

Siga estes passos para configurar o ambiente:

### 1. Instale o FFmpeg

FFmpeg é essencial para manipulação de vídeos. Para instalar, execute no terminal:

sudo dnf install ffmpeg

> 📝 Nota: Para outras opções de download, visite:
> - [FFmpeg - Download](https://ffmpeg.org/download.html)

### 2. Instale Git e Python 3.10

Se ainda não tiver Git e Python 3.10, instale-os com:

sudo dnf install git python310 python3-pip

> 📝 Nota:
> - Para outras opções de download do Git, visite [Git - Download](https://git-scm.com/)
> - Para Python 3.10, visite [Python 3.10 - Download](https://www.python.org/downloads/release/python-3106/)

### 3. Instale as Dependências Python

Execute o seguinte comando para instalar todas as dependências necessárias:

pip install sacremoses datasets deep-translator moviepy imageio imageio-ffmpeg huggingface-hub transformers torch datasets tqdm git+https://github.com/openai/whisper.git

## 🎬 Como Usar

Para usar o script, siga este formato:

python script.py <caminho_do_audio> <caminho_da_imagem> [-t]

- <caminho_do_audio>: O caminho para o seu arquivo de áudio (testado com arquivos .wav e .mp3, verifique para outros tipos de arquivo)
- <caminho_da_imagem>: O caminho para a imagem de fundo
- -t: (Opcional) Use esta flag se desejar que o texto seja traduzido para português

## 🔧 Solução de Problemas

Se encontrar algum problema:

1. Verifique se todas as dependências estão instaladas corretamente
2. Certifique-se de que os caminhos para o áudio e a imagem estão corretos
3. Verifique se o FFmpeg está instalado e acessível pelo terminal

- florencco