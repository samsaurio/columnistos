# -*- coding: utf-8 -*-
import scrapy
import logging
from scrapy.loader import ItemLoader
from diarios.items import DiariosItem

logging.basicConfig(level=logging.DEBUG)

class AbcSpider(scrapy.Spider):
    name = 'abc'
    allowed_domains = ['www.abc.com.py']
    start_urls = ['http://www.abc.com.py/edicion-impresa/opinion']
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }

    def parse(self, response):
        """
        @url http://www.abc.com.py/edicion-impresa/opinion
        @returns items 1 14
        @returns requests 0 0
        @scrapes author title url
        """
        # Esta búsqueda se queda con todo lo que tiene clase item-article y article-link
        # de esto busca todos los articulos
        selectors = response.xpath('//*[@class="item-article"]//*[@class="article-link"]')
        ind = 0
        for selector in selectors:
            link = response.urljoin(selector.xpath('.//@href').extract_first())
            if link is not None:
                yield scrapy.Request(link, callback=self.parse_article)
                ind=ind+1

    def parse_article(self, response):
        import re
        selector = response.xpath('//*[@class="article-container"]')
        loader = ItemLoader(DiariosItem(), selector=selector)

        # Busco y guardo autor
        autor = response.xpath('//*[@class="article-author"]/a/span/text()').extract_first().title().strip()
        autor = re.sub('[^a-zA-ZñÑáéíóúÁÉÍÓÚ ]', '', autor)
        loader.add_value('author', autor)

        # Guardo título
        loader.add_value('title', response.xpath('.//h1//text()').extract_first().strip())

        # Guardo URL
        loader.add_value('url', response.request.url)
        return loader.load_item()
