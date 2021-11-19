# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DxdoctorItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    provinceName = scrapy.Field()
    cities = scrapy.Field()
    currentConfirm = scrapy.Field()
    confirm = scrapy.Field()
    death = scrapy.Field()
    cure = scrapy.Field()
    # info = scrapy.Field()

    pass
