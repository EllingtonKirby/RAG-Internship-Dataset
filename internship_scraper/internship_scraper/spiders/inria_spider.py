from pathlib import Path
from re import *
import logging

import scrapy

class IasdInternshipSpider(scrapy.Spider):
    name = "inria"
    custom_settings = {
        "DOWNLOAD_DELAY": 0.1,
        "AUTOTHROTTLE_ENABLED":False
    }
    DOWNLOADER_MIDDLEWARES = {
        "scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware": 543,
    }   

    start_urls = ['https://recrutement.inria.fr/public/classic/fr/offres']

    # def __init__(self, *args, **kwargs):
    #     super(IasdInternshipSpider, self).__init__(*args, **kwargs)
    #     # Désactiver le mode debug
    #     logging.getLogger('scrapy').setLevel(logging.WARNING)

    def parse(self, response):
        offers = response.xpath("//div[@class='job-card']")
        for offer in offers:
            offer_link=offer.xpath("h2/a/@href").get().strip()
            yield response.follow(offer_link, callback=self.parse_offer)

    def parse_offer(self, offer):
        type=offer.xpath("normalize-space(//div[@class='grand-item-offre']/div[@class='item-offre']\
                         /p/text())").get().strip().lower()
        if type=='stage':
          title = offer.xpath("normalize-space(//h1/text())").get().strip()
          organization = offer.xpath("normalize-space(//div[h2='Informations générales']/ul/li/\
                                     a[@class='a-inria']/text())").get().strip()
          supervisor = offer.xpath("normalize-space(//div[h2='Contacts']/ul/li/strong[text()='Recruteur :']/\
                                   following-sibling::br/following-sibling::text())").get()[:-1].strip()
          context = offer.xpath("normalize-space(//div[h2='Contexte et atouts du poste']\
                                    //div)").get().strip()
          mission = offer.xpath("normalize-space(//div[h2='Mission confiée']\
                                    //div)").get().strip()
          description = context+"\n"+mission
          pdf_link = offer.xpath("//a[starts-with(@title, 'Télécharger')]/@href").get().strip()
          yield {
              'title': title,
              'organization': organization,
              'supervisor': supervisor,
              'description': description,
              'link': 'https://recrutement.inria.fr'+pdf_link
          }
