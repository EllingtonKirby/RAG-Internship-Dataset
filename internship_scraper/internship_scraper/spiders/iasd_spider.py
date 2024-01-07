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
        internships = response.xpath("//div[@class='internship']")
        for internship in  internships:
            yield self.parse_internship(internship)


    def parse_internship(self, internship):
        if internship.xpath("div[@class='internship-title']"): # check if internship is not already taken
            title = internship.xpath("normalize-space(div[@class='internship-title']/a/text())").get().strip()
            organization = internship.xpath("normalize-space(div[@class='internship-organization']/text())").get().strip()
            supervisor = internship.xpath("normalize-space(div[@classs='internship-supervisor']/text())").get().strip()
            description = ""
            pdf_link = internship.xpath("normalize-space(div[@class='internship-title']/a/@href)").get().strip()
            return {
                'title': title,
                'organization': organization,
                'supervisor': supervisor,
                'description': description,
                'link': pdf_link
            }
