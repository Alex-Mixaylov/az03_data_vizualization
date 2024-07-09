import scrapy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class DivansonlyparsSpider(scrapy.Spider):
    name = "divansonlypars"
    divans = []  # Список для хранения всех товаров

    def start_requests(self):
        urls = [
            "https://www.divan.ru/category/divany-i-kresla?types%5B%5D=1&types%5B%5D=4&types%5B%5D=54",
            "https://www.divan.ru/category/divany-i-kresla/page-2?types%5B%5D=1&types%5B%5D=4&types%5B%5D=54",
            "https://www.divan.ru/category/divany-i-kresla/page-3?types%5B%5D=1&types%5B%5D=4&types%5B%5D=54",
            "https://www.divan.ru/category/divany-i-kresla/page-4?types%5B%5D=1&types%5B%5D=4&types%5B%5D=54",
            "https://www.divan.ru/category/divany-i-kresla/page-5?types%5B%5D=1&types%5B%5D=4&types%5B%5D=54",
            "https://www.divan.ru/category/divany-i-kresla/page-6?types%5B%5D=1&types%5B%5D=4&types%5B%5D=54",
            "https://www.divan.ru/category/divany-i-kresla/page-7?types%5B%5D=1&types%5B%5D=4&types%5B%5D=54",
            "https://www.divan.ru/category/divany-i-kresla/page-8?types%5B%5D=1&types%5B%5D=4&types%5B%5D=54",
            "https://www.divan.ru/category/divany-i-kresla/page-9?types%5B%5D=1&types%5B%5D=4&types%5B%5D=54",
            "https://www.divan.ru/category/divany-i-kresla/page-10?types%5B%5D=1&types%5B%5D=4&types%5B%5D=54",
            "https://www.divan.ru/category/divany-i-kresla/page-11?types%5B%5D=1&types%5B%5D=4&types%5B%5D=54",
            "https://www.divan.ru/category/divany-i-kresla/page-13?types%5B%5D=1&types%5B%5D=4&types%5B%5D=54",
            "https://www.divan.ru/category/divany-i-kresla/page-14?types%5B%5D=1&types%5B%5D=4&types%5B%5D=54",
            "https://www.divan.ru/category/divany-i-kresla/page-15?types%5B%5D=1&types%5B%5D=4&types%5B%5D=54",
            "https://www.divan.ru/category/divany-i-kresla/page-16?types%5B%5D=1&types%5B%5D=4&types%5B%5D=54",
            "https://www.divan.ru/category/divany-i-kresla/page-17?types%5B%5D=1&types%5B%5D=4&types%5B%5D=54",
            "https://www.divan.ru/category/divany-i-kresla/page-18?types%5B%5D=1&types%5B%5D=4&types%5B%5D=54",
            "https://www.divan.ru/category/divany-i-kresla/page-19?types%5B%5D=1&types%5B%5D=4&types%5B%5D=54",
            "https://www.divan.ru/category/divany-i-kresla/page-20?types%5B%5D=1&types%5B%5D=4&types%5B%5D=54",
            "https://www.divan.ru/category/divany-i-kresla/page-21?types%5B%5D=1&types%5B%5D=4&types%5B%5D=54",
            "https://www.divan.ru/category/divany-i-kresla/page-22?types%5B%5D=1&types%5B%5D=4&types%5B%5D=54",
            "https://www.divan.ru/category/divany-i-kresla/page-23?types%5B%5D=1&types%5B%5D=4&types%5B%5D=54",
        ]
        for url in urls:
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

    def closed(self, reason):
        self.save_to_csv(reason)

        # Загрузка данных из CSV файла
        df = pd.read_csv("divans.csv")

        # Преобразование столбца 'price' к числовому формату с обработкой ошибок
        try:
            # Фильтрация корректных числовых значений в столбце 'price'
            df['price'] = df['price'].str.replace(' ', '')  # Удаление пробелов, если они есть
            df = df[pd.to_numeric(df['price'], errors='coerce').notnull()]  # Фильтрация корректных числовых значений
            df['price'] = pd.to_numeric(df['price']) # Преобразование столбца 'price' к числовому формату
        except pd.errors.ParserError as e:
            print(f"Ошибка при преобразовании столбца 'price': {e}")

        # Расчет средней цены с двумя знаками после запятой
        mean_price = df['price'].mean()
        mean_price_formatted = "{:.2f}".format(mean_price)
        print(f'Средняя цена товаров: {mean_price_formatted}')

        # Создание гистограммы цен
        plt.figure(figsize=(10, 6))
        plt.hist(df['price'], bins=20, color='skyblue', edgecolor='black')
        plt.xlabel('Цена')
        plt.ylabel('Частота')
        plt.title('Гистограмма цен на диваны на сайте divan.ru')
        plt.grid(True)

        # Добавление вертикальной линии для средней цены в гистограмму
        mean_price = df['price'].mean()
        plt.axvline(mean_price, color='red', linestyle='dashed', linewidth=1)
        plt.text(mean_price, 50, f'Средняя цена: {mean_price:.2f}', rotation=90, va='bottom', ha='right', color='red')

        plt.show()

    def save_to_csv(self, reason):
        self.logger.info(f'Паук завершил работу по причине: {reason}')

        # Сохранение данных в CSV файл после завершения парсинга всех страниц
        df = pd.DataFrame(self.divans)
        df.to_csv("divans.csv", index=False)

        # Вывод в терминал PyCharm количества записанных в файл товаров
        self.logger.info(f'Записано товаров в файл: {len(self.divans)}')
