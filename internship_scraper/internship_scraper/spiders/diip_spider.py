from pathlib import Path

import scrapy
import re

class IasdInternshipSpider(scrapy.Spider):
    name = "diip"
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
    }
    DOWNLOADER_MIDDLEWARES = {
        "scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware": 543,
    }   

    start_urls = ['https://u-paris.fr/diip/2024-internship-opportunities-for-masters-students/']

    def parse(self, response):
        num_internships = len(response.xpath("//div[@class='et_pb_column et_pb_column_3_4 et_pb_column_5    et_pb_css_mix_blend_mode_passthrough']/*"))
        for i in range(num_internships):
          internship = response.xpath(f"//div[@class='et_pb_module et_pb_toggle et_pb_toggle_{i} et_pb_toggle_item  et_pb_toggle_close']")
          yield self.parse_internship(internship)

    def parse_internship(self, internship):
      title = internship.xpath("normalize-space(h5[@class='et_pb_toggle_title']/text())").get().strip()
      supervisor = internship.xpath("normalize-space(div[@class='et_pb_toggle_content clearfix']/p/strong/text())").get().strip()
      description = internship.xpath("normalize-space(div[@class='et_pb_toggle_content clearfix']/p[2]/text())").get().strip()
      link = internship.xpath("div[@class='et_pb_toggle_content clearfix']/p/strong/a/@href").get().strip()
      result = re.search(r'\((.*?)\)', internship.xpath("normalize-space(div[@class='et_pb_toggle_content clearfix']/p)").get().strip())
      if result:
        organization = result.group(1)
      else:
         organization = ''
      return {
         'title':title,
         'organization':organization,
         'supervisor':supervisor,
         'description':description,
         'link':link
      }
      
 