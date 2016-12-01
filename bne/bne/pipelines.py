# -*- coding: utf-8 -*-
import csv
import json
from unidecode import unidecode

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class Cleanup(object):
    def process_item(self, item, spider):
        return {unidecode(k.lower()): str(v) for k, v in item.items()}


class Json(object):
    def open_spider(self, spider):
        self.stream = open('records.jl', 'w')

    def close_spider(self, spider):
        self.stream.close()

    def process_item(self, item, spider):
        self.stream.write(json.dumps(item) + '\n')
        return item
