from setuptools import setup, find_packages

setup(
    name="MP3praMP4",
    version="1.1.2",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "whisper",
        "torch",
        "transformers",
        "datasets",
        "tqdm",
        "sentencepiece",
        "sacremoses"
    ],
    entry_points={
        "console_scripts": [
            "mp3pramp4=mp3pramp4.cli:cli_entry"
        ]
    },
    include_package_data=True,
    zip_safe=False,
)