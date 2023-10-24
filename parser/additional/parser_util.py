import random

from urllib import parse
from typing import List, Dict
from pyppeteer import launch
from pyppeteer.browser import Browser
from pyppeteer.page import Page, ElementHandle


class ParsingNews:
    """
    Класс для парсинга новостей с сайта Bybit
    """
    def __init__(self):
        """
        Инициализирует класс
        """
        # Настройки браузера
        self.__executable_path = '/usr/bin/google-chrome-stable'
        self.headless = True
        self.autoClose = False
        self.args = ['--no-sandbox', '--disable-caches']

        # Настройки url адреса
        self.__base_url = 'https://announcements.bybit.com/en-US/'
        self.category = ''
        self.page = 1

    def get_header(page) -> dict:
        return {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
        }

    def response_predicate(self, response) -> bool:
        """
        Предсказывает ответ сервера
        """
        return response.status == 200

    async def start_browser(self) -> Browser:
        """
        Запускает браузер
        """
        return await launch(
            executablePath=self.__executable_path,
            args=self.args,
            headless=self.headless,
            autoClose=self.autoClose,
        )

    def construct_url(self) -> str:
        """
        Создает url для запроса. Добавляем version для обхода CDN кеша
        """
        params = {
            'category': self.category,
            'page': self.page,
            'v': random.randint(0, 9999)
        }
        return f'{self.__base_url}?{parse.urlencode(params)}'
    
    async def get_href(self, element: ElementHandle) -> str:
        """
        Достает href элемента
        """
        href_element = await element.getProperty('href')
        return await href_element.jsonValue()

    async def get_text_title(self, page: Page, element: ElementHandle) -> str:
        """
        Получает текст заголовка
        """
        title = await element.querySelector('span')
        return await page.evaluate('(element) => element.textContent', title)

    async def get_news(self, page: Page) -> List[Dict[str, str]]:
        """
        Парсим объявления со страницы
        """
        selector_all_news = 'div.article-list'
        selector_one_news = 'a.no-style'

        news = await page.waitForSelector(selector_all_news, {'timeout': 10000})
        topics = await news.querySelectorAll(selector_one_news)

        list = []

        for topic in topics:
            title = await self.get_text_title(page, topic)
            href = await self.get_href(topic)

            list.append({
                "href": href,
                "title": title,
            })
        return list