import asyncio
import time

from additional.redis_util import RedisProcess
from additional.parser_util import ParsingNews
from additional.csv_util import CSVProcess
from pyppeteer.browser import Browser


async def fetch(browser: Browser, parser_utils: ParsingNews, csv_utils: CSVProcess, 
                redis_utils: RedisProcess) -> None:
    """
    Каждый запрос парсит самое первое объявление и сохраняет его если оно уникальное
    """
    page = await browser.newPage()
    await page.setExtraHTTPHeaders(parser_utils.get_header())
    await page.goto(parser_utils.construct_url())
    await page.waitForResponse(urlOrPredicate=parser_utils.response_predicate)
    title, href = await parser_utils.get_news(page)

    exists = redis_utils.exists(title)

    if exists is None:
        redis_utils.save(title)
        csv_utils.add_record(title, href)
        print(f"Новая запись сохранена! Время запроса: {time.time()}")

    print(f'Объект существует. Время запроса: {time.time()}')

async def main() -> None:
    """
    Создает бесконечное количество запросов к bybit
    """
    parsing_time = 1
    redis_utils = RedisProcess()
    parser_utils = ParsingNews()
    csv_utils = CSVProcess()

    browser = await parser_utils.start_browser()

    try:
        while True:
            asyncio.gather(fetch(browser, parser_utils, csv_utils, redis_utils))
            await asyncio.sleep(parsing_time)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    asyncio.run(main())