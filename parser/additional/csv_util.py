import os
import csv

from datetime import datetime as dt


class CSVProcess:
    """
    Класс для работы с csv файлом.
    """
    def __init__(self):
        """
        Инициализирует класс
        """
        self.__name = 'topics.csv'
        self.__fieldnames = ['topic', 'link', 'time']

    def add_record(self, title: str, href: str) -> None:
        """
        Добавляет запись в файл CSV
        """
        record = {
            'topic': title,
            'link': href,
            'time': dt.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        with open(self.__name, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.__fieldnames)
            writer.writerow(record)