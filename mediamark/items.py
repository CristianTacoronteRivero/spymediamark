# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MediamarkItem(scrapy.Item):
    modelo = scrapy.Field()
    date_time = scrapy.Field()
    precio_anterior = scrapy.Field()
    precio_actual = scrapy.Field()

