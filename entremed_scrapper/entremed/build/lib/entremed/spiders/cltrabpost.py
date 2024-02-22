import scrapy
from .basespider import * 
from itemloaders.processors import MapCompose, TakeFirst, Join, Compose
import time



class CltrabpostSpider(BaseSpider):
    name = "cltrabpost"
    allowed_domains = ["www.chiletrabajos.cl"]

#   We define the name of the Webservice worked here
    web_service = "Chiletrabajo"

    def __init__(self, url='', id='', **kwargs):
        self.jwt = self.get_jwt()
        super().__init__(**kwargs)
        self.url = url
        self.id = id

#   This function defines the parameters for te scraping process and sets the urls to be analysed. Then, it invoques the parser function. 
    def start_requests(self):
        
#       We define the header that the scrapper will simulate. This is done so the target page thinks a legit browser is analysing it.
        headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br'}

#       The urls to fetch are saved in a list. 
        self.start_urls = self.url
        
#       Then, we rescue the individual values and scan every website
        for item in self.start_urls:
            posting_id = self.id
            url = self.url
            
            if PROXY_CHILETRABAJO == "ON":
                source_url = url
                url = self.create_proxy_link(url)
            else:
                url = url
                source_url = url
            yield scrapy.Request(url, headers=headers, cb_kwargs={'source_url':source_url,'id':posting_id},errback = self.errback_close_page,)


    def parse(self, response, source_url, id):

#       We log the open of the spider.        
        self.log_init(source_url)

#       We get the root and table variable to work with.
        root = response.css('div#detalle-oferta')
        table = root.xpath('.//div/div/table/tbody/tr')

#       We setup the item variable
        item = ItemLoader(item=RawJobItem(), selector=root)

        i = 0

        for row in table:
            item_check = row.xpath('.//td/text()').get()
            if item_check == "Salario":
                item.add_xpath('salary', f'.//*[{i+1}]/td/div/text()')
            if item_check == "Tipo":
                item.add_xpath('work_schedule', f'.//*[{i+1}]/td/a/text()')
            if item_check == "Duración":
                item.add_xpath('employment_type', f'.//*[{i+1}]/td/following-sibling::td/text()')
            if item_check == "Fecha":
                item.add_xpath('published_date', f'.//*[{i+1}]/td/following-sibling::td/div/text()')
            i = i + 1

        item.add_css('pills', 'div.botones-desc span::text', Compose(lambda v: " ".join(v)))
        item.add_css('title', 'h1.title::text')
        item.add_css('description', 'p.mb-0::text', Compose(lambda v: " ".join(v)))
        item.add_value('posting_url', source_url)
        item.add_value('id', id)

        yield item.load_item()








    async def errback_close_page(self, failure):
        self.log_scrapping_error(failure, self.web_service)
        return