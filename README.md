# 🎵 MP3 para MP4 Converter 📼

Este é um script avançado que transforma arquivos de áudio em vídeos com uma imagem de fundo estática e legendas em inglês ou português.

## 📋 Sumário

1. [Pré-requisitos](#pré-requisitos)
2. [Instalação](#instalação)
3. [Como Usar](#como-usar)
4. [Solução de Problemas](#solução-de-problemas)

## 🛠 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- Python 3.10 ou superior
- Git

> 📝 O FFmpeg será instalado automaticamente pelo `setup.py` durante a instalação do projeto.

## 🚀 Instalação

Siga estes passos para configurar o ambiente:

### 1. Clone o repositório

```sh
git clone https://github.com/seu-usuario/MP3praMP4.git
cd MP3praMP4
```

### 2. Instale o projeto

Execute o seguinte comando para instalar todas as dependências e o FFmpeg automaticamente:

```sh
pip install .
```

Isso instalará todas as dependências listadas no `requirements.txt` e também fará o download do FFmpeg conforme o sistema operacional.

## 🎬 Como Usar

Para converter um áudio em vídeo com legendas, utilize:

```sh
mp3pramp4 <caminho_do_audio> <caminho_da_imagem> [-t]
```

- `<caminho_do_audio>`: O caminho para o seu arquivo de áudio (testado com arquivos .wav e .mp3, verifique para outros tipos de arquivo)
- `<caminho_da_imagem>`: O caminho para a imagem de fundo
- `-t`: (Opcional) Use esta flag se desejar que o texto seja traduzido para português

Exemplo de uso:

```sh
mp3pramp4 meu_audio.mp3 minha_imagem.jpg -t
```

Isso irá gerar um vídeo MP4 com a imagem estática e legendas traduzidas para português.

## 🔧 Solução de Problemas

Se encontrar algum problema:

1. Verifique se todas as dependências foram instaladas corretamente
2. Certifique-se de que os caminhos para o áudio e a imagem estão corretos
3. Tente reinstalar o projeto com `pip install --force-reinstall .`
4. No Windows, verifique se o FFmpeg está instalado corretamente em `%USERPROFILE%\ffmpeg\bin`
5. No Linux, verifique se o FFmpeg está disponível em `~/.local/bin`

Se o problema persistir, abra uma issue no repositório do projeto.

### Por florencco 🎼
