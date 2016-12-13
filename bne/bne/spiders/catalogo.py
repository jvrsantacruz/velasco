# -*- coding: utf-8 -*-
import scrapy
from slugify import slugify

import velasco.parsing


class CatalogoSpider(scrapy.Spider):
    name = "catalogo"
    allowed_domains = ["catalogo.bne.es"]
    start_urls = ['http://catalogo.bne.es/']

    def __init__(self, metadata_path=None):
        if metadata_path is None:
            raise Exception('Missing metadata file')
        self.meta = list(velasco.parsing.parse_metadata(metadata_path))

    def parse(self, response):
        query = "//a[text()='Búsqueda por signatura']/@href"
        path = response.xpath(query)[0].extract()
        url = self.url(path)
        yield scrapy.Request(url=url, callback=self.search)


    def search(self, response):
        for entry in self.meta:
            if not entry['ref']:
                continue

            try:
                ref = 'MSS/' + str(int(entry['ref']))
            except ValueError:
                ref = str(entry['ref'])

            yield scrapy.FormRequest.from_response(
                response,
                formname='searchform',
                formdata={'searchdata1': ref},
                meta={'extra': {'id': entry['id'], 'ref': ref}},
                callback=self.search_result_or_record
            )

    def search_result_or_record(self, response):
        if list(response.css('ul.hit_list')):
            return self.search_results(response)

        if list(response.css('.viewmarctags')):
            return self.record(response)

        raise Exception('Unknown response')

    def search_results(self, response):
        ref = response.request.meta['extra']['ref']
        query = "//a[contains(text(), '{}')]/@href".format(ref)
        path = response.xpath(query)[0].extract()
        url = self.url(path)
        return scrapy.Request(url, meta=response.request.meta,
                              callback=self.search_result_or_record)

    def record(self, response):
        data = multidict(
            (slugify(clean(totext(th)), only_ascii=True), clean(totext(td)))
            for th, td in pairs(response.css('.viewmarctags'))
        )
        data.update(response.request.meta['extra'])
        return data

    def url(self, *pieces):
        return urljoin('http://' + self.allowed_domains[0], *pieces)


def multidict(items):
    data = {}
    for key, value in items:
        if key in data:
            data[key] += ';' + value
        else:
            data[key] = value
    return data


def urljoin(*pieces):
    return "/".join(p.strip("/") for p in pieces)


def clean(text):
    return text.strip('\n:. ')


def totext(e):
    return e.root.xpath('string()').strip()


def pairs(sequence):
    seq = iter(sequence)
    while seq:
        yield next(seq), next(seq)
