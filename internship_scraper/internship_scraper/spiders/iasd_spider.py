from pathlib import Path

import scrapy

class IasdInternshipSpider(scrapy.Spider):
    name = "iasd"
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
    }
    DOWNLOADER_MIDDLEWARES = {
        "scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware": 543,
    }   

    start_urls = ['https://www.lamsade.dauphine.fr/wp/iasd/en/liste-des-stages-disponibles/']

    def parse(self, response):
        yield 0
