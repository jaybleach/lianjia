# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class LianjiaItem(Item):
    collection = 'details'
    title = Field()
    houseInfo = Field()
    positionInfo = Field()
    followInfo = Field()
    tag = Field()
    total = Field()
    unit = Field()
    detail_url = Field()

