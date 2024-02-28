import scrapy
from entremed.items import CompuTrabItemLoader
from .basespider import * 
from entremed.constants import *
from entremed.global_functions import handle_parsing_error
from itemloaders.processors import Compose
import re

class ComputrabpostSpider(BaseSpider):
    name = "computrabpost"
    allowed_domains = ["www.computrabajo.cl"]

#   We define the name of the Webservice worked here
    posting_service = "Computrabajo"

    def __init__(self, url='', id='', **kwargs):
        super().__init__(**kwargs)
        self.url = url
        self.id = id

#   This function defines the parameters for te scraping process and sets the urls to be analysed. Then, it invoques the parser function. 
    def start_requests(self):
        
#   We define the header that the scrapper will simulate. This is done so 
#   the target page thinks a legit browser is requesting it.
        headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 \
                    Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;\
                    q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,\
                    application/signed-exchange;v=b3;q=0.9',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br'}

#       The urls to fetch are saved in a list. 
        self.start_urls = self.url
        
#       Then, we rescue the individual values and scan every website
       
        posting_id = self.id
        url = self.url
        
        if PROXY_COMPUTRABAJO == "ON":
            source_url = url
            url = self.create_proxy_link(source_url)
        else:
            source_url = url
        yield scrapy.Request(url,
                             headers=headers,
                             cb_kwargs={'source_url':source_url,'id':posting_id},
                             errback = self.errback_close_page,)


    def parse(self, response, source_url, id):

#       We log the open of the spider.        
        self.log_init(source_url)

#       Now we initiate the scrapping of the information for the location. We get the root data to work with, 
#       that is, the basic chuncks of data that serves as resource to work. We then check what is missing and with 
#       that we proceed to analyse.  

        temp_title = response.css('div.container').xpath('.//h1/text()').get()
        if not temp_title:
            handle_parsing_error(self, None, self.posting_service, "DOMError", source_url)

        root = response.css('div.box_detail')
        pills = root.xpath('.//*[5]/div/span/text()').getall()
        extras = root.xpath('.//*[5]/ul//text()').getall()

#       We setup the item variable
        item = CompuTrabItemLoader(selector=root)

        item.add_xpath('description', './/*[5]/p/text()', Compose(lambda v: v[0:-4]))
        item.add_xpath('pills', './/*[5]/div/span/text()')
        
        for row in pills:
            if re.search(r'jornada',row,re.IGNORECASE):
                item.add_value('work_schedule', row)
            if re.search(r'conducir',row,re.IGNORECASE):
                item.add_value('driving_level', row)
            if re.search(r'discapacidad',row,re.IGNORECASE):
                item.add_value('inclusive_posting', row)
            if re.search(r'$',row,re.IGNORECASE):
                item.add_value('salary', row)
            if re.search(r'contrato|honorario.',row,re.IGNORECASE):
                item.add_value('employment_type', row)

        temp_extras = " ".join(extras).strip().replace("\'", "") if extras else None
        item.add_value('requisites', temp_extras) 
        item.add_value('id', id)

        yield item.load_item()








    async def errback_close_page(self, failure):
        handle_parsing_error(self, failure, self.posting_service, "OtherError", None)
        return