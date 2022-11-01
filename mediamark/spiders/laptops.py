import scrapy
from numpy import nan
from datetime import datetime
from mediamark.items import MediamarkItem

#  scrapy shell -s USER_AGENT='custom user agent' 'http://www.example.com'


def precios_item(extract):
    """Separa el precio anterior y actual del item seleccionado.
    Si solo tiene un precio, devuelve ese y como segundo valor devuelve Not a Number

    :param extract: Contiene los precios del item
    :type extract: List[str]
    :return: Devuelve los precios del item por separado
    :rtype: float
    """
    if len(extract) > 1:
        return float(extract[0]), float(extract[1])
    else:
        return nan, float(extract[0])

class LaptopsSpider(scrapy.Spider):
    name = 'laptops'
    allowed_domains = ['www.mediamarkt.es']
    url = 'https://www.mediamarkt.es/es/category/port%C3%A1tiles-153.html'
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = f'dirlog/{today}.log'
    custom_settings = {'LOG_LEVEL': 'INFO', 'LOG_FILE': log_file}

    def start_requests(self):
        utc_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        yield scrapy.Request(
                url=self.url,
                headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
                },
                callback=self.parse,
                meta = {
                    'utc_time': utc_time
                }
        )

    def parse(self, response):
        utc_time = response.meta['utc_time']
        item = MediamarkItem()

        for dato in response.xpath('//*[@data-test="mms-search-srp-productlist-item"]'):
            item['utctime'] = utc_time
            item['modelo'] = dato.xpath('.//p/text()').get()

            precio_anterior, precio_actual = precios_item(dato.xpath('.//span[2]/text()').extract())
            item['precio_anterior'] = precio_anterior
            item['precio_actual'] = precio_actual

            yield item
