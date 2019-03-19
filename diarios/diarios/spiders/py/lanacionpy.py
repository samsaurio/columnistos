# -*- coding: utf-8 -*-
import scrapy
import logging
from scrapy.loader import ItemLoader
from diarios.items import DiariosItem

logging.basicConfig(level=logging.DEBUG)

class LanacionpySpider(scrapy.Spider):
    name = 'lanacionpy'
    allowed_domains = ['www.lanacion.com.py']
    start_urls = ['https://www.lanacion.com.py/category/columnistas']
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }

    def parse(self, response):
        """
        @url https://www.lanacion.com.py/category/columnistas
        @returns items 1 14
        @returns requests 0 0
        @scrapes author title url
        """
        # Esta búsqueda se queda con todo lo que está debajo del arbol cuya id es west (panel principal)
        # de esto busca todos los articulos, pero filtra el primer div y el enlace
        selectors = response.xpath('//*[@id="west"]//article/div/a[2]')
        ind = 0
        for selector in selectors:
            link = response.urljoin(selector.xpath('.//@href').extract_first())
            if link is not None:
                yield scrapy.Request(link, callback=self.parse_article)
            ind=ind+1
        print (">>>> Artículos encontrados: ")
        print (ind)


    def parse_article(self, response):
        import re
        selector = response.xpath('//*[@id="article-content"]')
        loader = ItemLoader(DiariosItem(), selector=selector)
        #Extraigo autor y convierto en mayus y borro espacios
        autor = response.xpath('.//span[@class="author-name"]//text()').extract_first().title().strip()
        # Saco símbolos raros
        autor = re.sub('[^a-zA-ZñÑáéíóúÁÉÍÓÚ ]', '', autor)
        # Trae "Por" al principio así que lo saco
        if autor[:4] == "Por ":
             autor = autor[4:]
        # Guardo autor
        loader.add_value('author', autor)
        # Guardo título
        loader.add_value('title', response.xpath('//*[@class="title"]/h1/text()').extract_first().strip())
        # Guardo URL
        loader.add_value('url', response.request.url)
        return loader.load_item()
