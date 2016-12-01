# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Record(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    def parse(self, item, response):
        tags = response.css('.viewmarctags')
        if not tags:
            raise scrapy.exceptions.DropItem('Not single item view')

        yield {clean(totext(th)): clean(totext(td)) for th, td in pairs(tags)}
