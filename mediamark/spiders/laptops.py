import scrapy


class LaptopsSpider(scrapy.Spider):
    name = 'laptops'
    allowed_domains = ['www.mediamarkt.es']
    start_urls = ['https://www.mediamarkt.es/es/category/port%C3%A1tiles-153.html']

    def parse(self, response):
        title = response.xpath('//h1/text()').get()

        yield {
            '-------- titulo -------':title
        }
