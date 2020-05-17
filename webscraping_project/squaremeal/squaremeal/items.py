# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SquaremealItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    cuisine = scrapy.Field()
    price = scrapy.Field()
    num_reviews = scrapy.Field()
    stars = scrapy.Field()
