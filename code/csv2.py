# Copyright (c) 2023 Alex Krol - https://twitter.com/old_alexeykrol
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


# This script is designed to translate text from Russian to English within a CSV file using the OpenAI's GPT-4 model.
# Below is a detailed explanation of the code in both English and Russian.

# English:

# 1. Imports:
# - The `csv` module is used for reading from and writing to CSV files.
# - The `openai` module provides access to OpenAI's API.
# - The `nltk` module and `sent_tokenize` are used for natural language processing, specifically for tokenizing text into sentences.

# 2. Constants:
# - `RED_TEXT` and `RESET_TEXT` are ANSI escape codes for changing text color in the console, used here to highlight error messages.

# 3. Setup:
# - `nltk.download('punkt')` downloads the Punkt tokenizer models used by `nltk` for sentence splitting.
# - `openai.api_key` is set to your API key for OpenAI services.

# 4. Function - `split_text`:
# - This function splits a given text into chunks of sentences without exceeding a specified maximum length. This is necessary to comply with the token limits of the OpenAI API.

# 5. Function - `translate_to_english`:
# - Attempts to translate the given Russian text to English using the OpenAI API.
# - It splits the text into manageable chunks, sends them to the OpenAI API for translation, and then combines the translated chunks.
# - If an error occurs during the translation, it prints the error message in red text and returns `None`.

# 6. CSV Processing:
# - Opens the source CSV file `feedback.csv` for reading and creates a new CSV file `eng_feedback.csv` for the translated English feedback.
# - Reads the headers from the source CSV and writes them to the new CSV file.
# - Iterates through each row and cell of the source CSV, attempting to translate each cell's text to English.
# - If a translation fails, it retries up to 3 times. If all retries fail, it records an empty string for that cell in the new CSV file.

# 7. Error Handling:
# - If there are errors during translation, the script will print out the error message in red to make it visible and will insert an empty string for that cell in the new file.

# Russian:

# 1. Импорты:
# - Модуль `csv` используется для чтения и записи файлов CSV.
# - Модуль `openai` предоставляет доступ к API OpenAI.
# - Модуль `nltk` и функция `sent_tokenize` используются для обработки естественного языка, в частности, для разделения текста на предложения.

# 2. Константы:
# - `RED_TEXT` и `RESET_TEXT` — ANSI коды для изменения цвета текста в консоли, используются здесь для выделения сообщений об ошибках.

# 3. Настройка:
# - `nltk.download('punkt')` загружает модели токенизатора Punkt, используемые `nltk` для разделения на предложения.
# - `openai.api_key` задает ваш ключ API для сервисов OpenAI.

# 4. Функция - `split_text`:
# - Функция разбивает заданный текст на фрагменты предложений так, чтобы не превышать указанную максимальную длину. Это необходимо для соблюдения лимита токенов API OpenAI.

# 5. Функция - `translate_to_english`:
# - Пытается перевести данный русский текст на английский язык с использованием API OpenAI.
# - Текст разбивается на управляемые фрагменты, которые отправляются в API OpenAI для перевода, а затем объединяются переведенные фрагменты.
# - В случае возникновения ошибки во время перевода, скрипт печатает сообщение об ошибке красным цветом и возвращает `None`.

# 6. Обработка CSV:
# - Открывает исходный файл CSV `feedback.csv` для чтения и создает новый файл CSV `eng_feedback.csv` для переведенной на английский обратной связи.
# - Читает заголовки из исходного файла CSV и записывает их в новый файл CSV.
# - Проходит по каждой строке и ячейке исходного файла CSV, пытаясь перевести текст каждой ячейки на английский.
# - Если перевод не удается, он повторяет попытку до 3 раз. Если все попытки неудачны, он записывает пустую строку для этой ячейки в новый файл CSV.

# 7. Обработка Ошибок:
# - Если во время перевода возникают ошибки, скрипт будет печатать сообщение об ошибке красным цветом, чтобы оно было заметно, и будет вставлять пустую строку для этой ячейки в новый файл.



import csv
import openai
import nltk
from nltk.tokenize import sent_tokenize

# ANSI escape код для красного текста
RED_TEXT = "\033[31m"
RESET_TEXT = "\033[0m"

nltk.download('punkt')

openai.api_key = "....."

# Функция для разбиения текста на части предложениями
def split_text(text, max_length):
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_length:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

# Функция для перевода текста на английский с использованием OpenAI
def translate_to_english(text):
    try:
        translated_text = ""
        chunks = split_text(text, 500)
        print("Original text to translate:")
        print(text)
        print("\nSplit into chunks:")
        for chunk in chunks:
            print(f"- {chunk}")

        for chunk in chunks:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Translate the following Russian text to English:"},
                    {"role": "user", "content": chunk}
                ],
                temperature=0,
                max_tokens=500
            )
            translated_chunk = response.choices[0].message['content']
            print("\nTranslated chunk:")
            print(translated_chunk)
            translated_text += translated_chunk + " "
        
        print("\nFinal translated text:")
        print(translated_text.strip())
        return translated_text.strip()
    except Exception as e:
        print(f"{RED_TEXT}An error occurred: {e}{RESET_TEXT}")
        return None

# Открытие исходного CSV файла и создание нового для английских отзывов
with open('feedback.csv', mode='r', encoding='utf-8') as csvfile, \
     open('eng_feedback.csv', mode='w', encoding='utf-8', newline='') as eng_csvfile:
    
    csv_reader = csv.reader(csvfile)
    csv_writer = csv.writer(eng_csvfile)
    
    headers = next(csv_reader)
    csv_writer.writerow(headers)

    for row_index, row in enumerate(csv_reader, start=1):
        translated_row = []
        for cell_index, cell in enumerate(row):
            print(f"Processing row {row_index}, cell {cell_index}: '{cell}'")
            translation = translate_to_english(cell)
            if translation is not None:
                translated_row.append(translation)
            else:
                successful_translation = False
                attempts = 3  # Установите количество попыток
                for attempt in range(attempts):
                    try:
                        print(f"Retry {attempt+1} for cell {cell_index}...")
                        translation = translate_to_english(cell)
                        if translation is not None:
                            translated_row.append(translation)
                            successful_translation = True
                            break  # Выходим из цикла если перевод успешен
                    except Exception as retry_e:
                        print(f"Retry {attempt+1} at row {row_index}, cell {cell_index} failed: {retry_e}")
                if not successful_translation:
                    translated_row.append("")  # Добавляем пустую строку, если не удалось перевести
                    print(f"{RED_TEXT}All retries failed for cell {cell_index}. Adding empty string to the row.{RESET_TEXT}")
        csv_writer.writerow(translated_row)

