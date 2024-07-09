import scrapy
import pandas as pd

class DivansonlyparsSpider(scrapy.Spider):
    name = "divansonlypars"
    divans = []  # Список для хранения всех товаров

    def start_requests(self):
        base_url = "https://www.divan.ru/category/divany-i-kresla/page-{page}?types%5B%5D=1&types%5B%5D=4&types%5B%5D=54"
        # Генерация start_urls для страниц с 1 по 23
        for page in range(1, 24):
            url = base_url.format(page=page)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Проверка на наличие ошибки 404
        if response.status == 404:
            self.logger.info("Страница не найдена: %s", response.url)
            return

        # Парсинг товаров на текущей странице
        for divan in response.css('div._Ud0k'):
            item = {
                'name': divan.css('div.lsooF span::text').get(),
                'price': divan.css('div.pY3d2 span.ui-LD-ZU.KIkOH::text').get(),
                'price_old': divan.css('div.pY3d2 span.ui-LD-ZU.ui-SVNym.bSEDs::text').get(default='0'),
                'sale': divan.css('div.pY3d2 div.ui-JhLQ7::text').get(default='нет скидки'),
                'url': response.urljoin(divan.css('a::attr(href)').get())
            }
            self.divans.append(item)  # Добавление товара в общий список

            # Вывод в терминал PyCharm количества спарсенных товаров
            self.logger.info(f'Спарсено товаров: {len(self.divans)}')

            yield item

    def save_to_csv(self, reason):
        self.logger.info(f'Паук завершил работу по причине: {reason}')

        # Сохранение данных в CSV файл после завершения парсинга всех страниц
        df = pd.DataFrame(self.divans)
        df.to_csv("divans.csv", index=False)

        # Вывод в терминал PyCharm количества записанных в файл товаров
        self.logger.info(f'Записано товаров в файл: {len(self.divans)}')
