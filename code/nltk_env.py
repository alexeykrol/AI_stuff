import nltk

# Проверяем установлена ли библиотека NLTK
try:
    # Попытка импортировать nltk
    import nltk
    print("NLTK is installed.")
except ImportError as e:
    # Если импорт не удался, выводим сообщение об ошибке и инструкцию по установке
    print("NLTK is not installed. Install it by running 'pip install nltk'")

# Загружаем необходимые ресурсы NLTK для работы с русским языком
nltk.download('punkt')  # Токенизатор предложений
nltk.download('stopwords')  # Список стоп-слов
nltk.download('averaged_perceptron_tagger_ru')  # POS-таггер для русского языка

# Проверяем наличие русских стоп-слов
from nltk.corpus import stopwords
print(stopwords.words('russian'))

# Тестирование токенизации предложений
from nltk.tokenize import word_tokenize, sent_tokenize

text = "Привет, как дела? Я изучаю NLTK."
sentences = sent_tokenize(text, language='russian')
print(sentences)
