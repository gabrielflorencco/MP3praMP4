from setuptools import setup, find_packages
import os
import subprocess
import sys
import platform

def install_ffmpeg():
    """Baixa e instala o FFmpeg de acordo com o sistema operacional."""
    system = platform.system()

    if system == "Linux":
        ffmpeg_url = "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz"
        install_dir = os.path.expanduser("~/.local/bin")
        os.makedirs(install_dir, exist_ok=True)

        if not os.path.exists(os.path.join(install_dir, "ffmpeg")):
            print("Baixando e instalando FFmpeg para Linux...")
            subprocess.run(f"curl -L {ffmpeg_url} | tar -xJ --strip-components=1 -C {install_dir}", shell=True, check=True)
            print(f"FFmpeg instalado em {install_dir}")
        else:
            print("FFmpeg já está instalado.")
        
        os.environ["PATH"] += os.pathsep + install_dir

    elif system == "Windows":
        ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        install_dir = os.path.join(os.getenv("USERPROFILE"), "ffmpeg")

        if not os.path.exists(install_dir):
            print("Baixando e instalando FFmpeg para Windows...")
            temp_zip = os.path.join(os.getenv("TEMP"), "ffmpeg.zip")
            subprocess.run(f"curl -L {ffmpeg_url} -o {temp_zip}", shell=True, check=True)
            subprocess.run(f"powershell -Command \"Expand-Archive -Path '{temp_zip}' -DestinationPath '{install_dir}' -Force\"", shell=True, check=True)
            
            # Encontrar a pasta correta dentro da extração
            extracted_dirs = [d for d in os.listdir(install_dir) if os.path.isdir(os.path.join(install_dir, d))]
            if extracted_dirs:
                extracted_ffmpeg = os.path.join(install_dir, extracted_dirs[0], "bin")
                os.environ["PATH"] += os.pathsep + extracted_ffmpeg
                print(f"FFmpeg instalado em {extracted_ffmpeg}")
        else:
            print("FFmpeg já está instalado.")
    else:
        print("Sistema operacional não suportado para instalação automática do FFmpeg.")

def install_requirements():
    """Instala os pacotes listados no requirements.txt."""
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)

setup(
    name="MP3praMP4",
    version="1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],
    entry_points={
        "console_scripts": [
            "mp3pramp4 = main:main"
        ]
    },
    include_package_data=True,
    zip_safe=False,
)

if __name__ == "__main__":
    install_requirements()
    install_ffmpeg()
