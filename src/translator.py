import torch
from transformers import pipeline
from datasets import Dataset
      # GPU                                # CPU
device = 0 if torch.cuda.is_available() else -1

translator_pipeline = pipeline("translation", model="Helsinki-NLP/opus-mt-tc-big-en-pt", device=device)

def translate_batch(batch):
    """Função auxiliar para tradução em lote utilizada pelo método map do Hugging Face Datasets."""
    translations = translator_pipeline(batch['text'], max_length=40)
    return {'translated_text': [translation['translation_text'] for translation in translations]}

def translate_texts(texts):
    """
    Traduz uma lista de textos.
    
    Utiliza o Hugging Face Dataset para aplicar a tradução de forma batched.
    """
    dataset = Dataset.from_dict({'text': texts})
    translated_dataset = dataset.map(translate_batch, batched=True, batch_size=8)
    return translated_dataset['translated_text']
