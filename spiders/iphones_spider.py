# -*- coding: utf-8 -*-
import scrapy
from ..items import IphonesItem


class IphonesSpider(scrapy.Spider):
    name = 'iphones'
    start_urls = ['https://shop.mts.ru/catalog/smartfony/apple/']

    def parse(self, response):
        for href in response.css('.fit-block a::attr(href)'):
            yield response.follow(href, self.parse_iphone)

        for href in response.css('li.next a::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_iphone(self, response):
        items = IphonesItem()

        name = response.css('h1::text').getall()[2].strip()

        pattern = r"'price': ([0-9]+),"
        price = response.css('script::text').re_first(pattern)
        price = float(price)

        picture = response.css('link[itemprop="image"]::attr(href)').get().replace(r'"', '')

        specs_list = response.css('td.name, td.value').css('::text').getall()
        specs = {specs_list[i]: specs_list[i+1] for i in range(0, len(specs_list), 2)}

        items['name'] = name
        items['price'] = f'{price:.2f}'
        items['picture'] = picture
        items['specs'] = specs

        yield items
