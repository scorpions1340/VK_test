"""Так как в тексте задания не сказано, можно ли пользоваться сторонними библиотеками, для разбивания текста и обработки
вводных слов будем пользоваться специальными библиотекми"""
import pandas as pd  # для более простой работы с форматом csv
import nltk  # для обработки текста
from nltk.tokenize import sent_tokenize  # для правильного разбиения на предложения
from tqdm import trange  # добавляем красивый вывод в консоль


def AI_Downloader():
    """Загрузка нужных моделей обработки текста"""
    nltk.download('averaged_perceptron_tagger')
    nltk.download('punkt')


class CsvRedactor:  # основной класс для работы с csv-файлами, получения столбцов и тп.
    def __init__(self, file_path):
        """конструктор класса"""
        self.file_path = file_path  # запросим путь к файлу для обработки
        self.data_frame = pd.read_csv(self.file_path, usecols=['id', 'label', 'text', 'introduction'],
                                      dtype={'id': int, 'label': str, 'text': str, 'introduction': str})  # открытие
        # файла формата csv с помощью библиотеки pandas
        self.data_frame['introduction'] = 'Нет данных'  # заполняем ячейки столбца 'introduction', как "Нет данных"
        self.introductory_words = {'dear', 'hello', 'hi', 'hey', 'to', 'greetings',
                     'good morning', 'good afternoon', 'good evening', 'hi there',
                     'dear', 'hi everyone', 'dear team', 'hi all',
                     'hello team', 'dear colleagues', 'dear mr.', 'dear mrs.',
                     'dear ms.', 'dear dr.', 'attention', 'dear hiring manager',
                     'dear hiring committee', 'dear recruiting team',
                     'dear selection committee', 'hello hr', 'dear human resources',
                     'hello sales team', 'dear accounting department',
                     'hello marketing team', 'dear legal department',
                     'dear customer service team', 'dear support team', 'thanks'}  # фильтр вводных слов

    def get_column(self, column_name: str = "text") -> str:
        """получаем текст для каждой записи в csv файле"""
        text = self.data_frame[column_name]
        return text

    def AI_intro_searcher(self, text):
        """Удаление фрагментов текста, содержащих вводные слова"""
        sentences = sent_tokenize(text)  # Разбиваем текст на предложения
        result = []
        filtered_sentense = []
        for sentence in sentences:  # проходимся по предложениям
            words = nltk.word_tokenize(sentence)
            # получаем слова из предложения, конечно, самый простой способ - проверять первое слово в предложении,
            # но оно может быть и в середине предложения, поэтому...
            filtered = True  # создаем флаг, для отслеживания вводных слов в предложениях

            for word in words:
                # проходимся по всем словам в каждом предложении (затраты памяти и времени -
                # колоссальны (´;ω;) （>﹏<） (ಥ﹏ಥ), но это наш путь, чтобы ничего не упустить...)

                if word.lower() in self.introductory_words:  # проверяем, является ли слово вводным
                    filtered = False  # меняем флаг - значит, что в предложении есть вводное слово

            if filtered:  # исходя из наличия вводных слов заполняем нужный массив
                result.append(sentence)  # позже - не понадобится
            else:
                filtered_sentense.append(sentence)
        return ' '.join(result), ' '.join(filtered_sentense)  # возвратим получившиеся списки


def main():
    """основные блоки работы программы"""
    AI_Downloader()  # загружаем модели
    email_file = CsvRedactor(file_path="emailTextsI.csv")  # считываем файл в переменную df
    text = email_file.get_column("text")  # получаем ячейки столбца 'text'
    for el in trange(len(text), desc="Фильтрация сообщений(Отфильтровано/Всего)"):
        if isinstance(text[el], str):  # проверяем, что в строке 'text' есть текст
            result, filtered = email_file.AI_intro_searcher(text[el])  # получаем отфильтрованный текст
            email_file.data_frame.iat[el, 3] = filtered  # запись элемента в столбец 'introduction'
        else:
            print("Элемент не является строкой: ", text[el], "id = ", el)
    email_file.data_frame.to_csv("output.csv", encoding="utf-8", index=False)  # запись файла


if __name__ == "__main__":  # точка входа программы
    main()

