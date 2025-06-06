# -*- coding: utf-8 -*-
"""Classifier.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ldw6PIFMx-3Skj4tsUaXjDLvPZh4C57B
"""

# Commented out IPython magic to ensure Python compatibility.
# %%python -m pip install pip<24.1

# Commented out IPython magic to ensure Python compatibility.
# %pip install langdetect

"""Импорт textract"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install textract
import textract

"""Загрузка BERT"""

from transformers import BertTokenizer, BertForSequenceClassification, pipeline
import torch

# Загрузка предобученной модели и токенизатора
model_name = 'bert-base-multilingual-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
class_model = BertForSequenceClassification.from_pretrained(model_name, num_labels=3)
"""
    #Инициализация мультиязычных моделей
    # Классификатор
    tokenizer = BertTokenizer.from_pretrained("bert-base-multilingual-cased")
    classifier = BertForSequenceClassification.from_pretrained(
        "bert-base-multilingual-cased",
        num_labels=len(CLASS_NAMES)
    )
"""
# Для английского
en_summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Для русского
ru_summarizer = pipeline(
    "summarization",
    model="IlyaGusev/rut5_base_sum_gazeta",
    tokenizer="IlyaGusev/mbart_ru_sum_gazeta"
)

def summarize_text(text, summarizer):
    """Генерация краткого описания"""
    try:
        summary = summarizer(
          text[:2000] if len(text) > 20 else text,
          max_length=15,
          min_length=3,
          length_penalty=0.2  # Делаем суммаризацию короче
        )        # Для очень длинных текстов берем первые 1000 токенов
        return summary[0]['summary_text']
    except Exception as e:
        print(f"Summarization error: {e}")
        return "No summary available"

def DefineCluster(text, directory, filename):
  # Текст для классификации
  #text = "Article: reasearch the effect of garbage on the human psyche"

  # Токенизация и подготовка входа
  inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)

  # Классификация
  with torch.no_grad():
      outputs = class_model(**inputs)
      predictions = torch.argmax(outputs.logits, dim=1)

  # Соответствие меток
  labels = ["email", "scientific_article", "resume"]
  predicted_label = labels[predictions.item()]

  print(f"\nDocument classified as: {predicted_label}")

   # Вызов соответствующей функции обработки
  if predicted_label == "email":
    source_file = filename
    destination_path = "/content/drive/MyDrive/emails"

    # Создать папку, если её нет
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    begPath = directory + '/' + filename
    shutil.copy(begPath, '/content/drive/MyDrive/emails')  #  os.rename(source_file, destination_path)
    print(f"Файл перемещён в {destination_path}")

  elif predicted_label == "scientific_article":
    source_file = filename
    destination_path = "/content/drive/MyDrive/scientific_article"

    # Создать папку, если её нет
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    begPath = directory + '/' + filename
    shutil.copy(begPath, '/content/drive/MyDrive/scientific_article')  #  os.rename(source_file, destination_path)
    print(f"Файл перемещён в {destination_path}")

  elif predicted_label == "resume":
    source_file = filename
    destination_path = "/content/drive/MyDrive/resume"

    # Создать папку, если её нет
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    begPath = directory + '/' + filename
    shutil.copy(begPath, '/content/drive/MyDrive/resume')  #  os.rename(source_file, destination_path)
    print(f"Файл перемещён в {destination_path}")
  else:
        print("Unknown document type")

from langdetect import detect

def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

from google.colab import drive
drive.mount('/content/drive', force_remount=True)

import os
import shutil

# Путь к папке с файлами
folder_path = "/content/drive/MyDrive/InputData"

# Поддерживаемые форматы
supported_extensions = ['.pdf', '.docx', '.txt', '.pptx', '.jpg', '.png', '.jpeg']

# Проходим по всем файлам в папке
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)

    # Проверяем расширение файла
    if os.path.isfile(file_path) and any(file_path.lower().endswith(ext) for ext in supported_extensions):
        try:
          print(f"Обработка файла: {filename}...")

          # Извлекаем текст
          text = textract.process(file_path).decode('utf-8')
          if (filename == "Re_ Сдача по Защите информации.pdf"):
            print(text)

          # Определяем язык
          text_lang = detect_language(text)

          # Определение краткого описания текста
          if (text_lang == "ru"):
            print(summarize_text(text, ru_summarizer))
          elif (text_lang == "en"):
            print(summarize_text(text, en_summarizer))

          # Делим на кластеры
          DefineCluster(text, folder_path, filename)






        except ValueError:
          print("ERROR")

"""Определение кластера текста с помощью BERT"""