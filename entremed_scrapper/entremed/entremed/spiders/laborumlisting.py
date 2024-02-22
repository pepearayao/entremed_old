import scrapy
from entremed.items import LaborumItemLoader
from .basespider import * 
from entremed.constants import *
from entremed.global_functions import handle_parsing_error
from itemloaders.processors import MapCompose, Compose
from playwright.sync_api import Playwright, sync_playwright, expect
from scrapy.crawler import CrawlerProcess
from scrapy_playwright.page import PageMethod


class LaborumlistingSpider(BaseSpider):
    name = "laborumlisting"
    allowed_domains = ["www.laborum.cl"]

#   We define the name of the Webservice worked here.
    posting_service = "Laborum"

#   This function defines the parameters for te scraping process and sets the 
#   urls to be analysed. Then, it invoques the parser function. 
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
        
#   The urls to fetch are saved in a list. 
        self.start_urls = [
            "https://www.laborum.cl/empleos-busqueda-enfermera.html?recientes=true",
            # "https://www.laborum.cl/empleos-busqueda-enfermeria.html?recientes=true",
            # "https://www.laborum.cl/empleos-busqueda-tens.html?recientes=true",
            # "https://www.laborum.cl/empleos-busqueda-tecnico-enfermeria.html?recientes=true",
            # "https://www.laborum.cl/empleos-busqueda-psicologo.html?recientes=true",
            # "https://www.laborum.cl/empleos-busqueda-psicologia.html?recientes=true",
            # "https://www.laborum.cl/empleos-busqueda-odontologo.html?recientes=true",
            # "https://www.laborum.cl/empleos-busqueda-odontologia.html?recientes=true",
            # "https://www.laborum.cl/empleos-busqueda-kinesiologo.html?recientes=true",
            # "https://www.laborum.cl/empleos-busqueda-kinesiologia.html?recientes=true",
            # "https://www.laborum.cl/empleos-busqueda-psicopedagogo.html?recientes=true",
            # "https://www.laborum.cl/empleos-busqueda-psicopedagogia.html?recientes=true",
            # "https://www.laborum.cl/empleos-busqueda-fonoaudiologo.html?recientes=true",
            # "https://www.laborum.cl/empleos-busqueda-fonoaudiologia.html?recientes=true",
            # "https://www.laborum.cl/empleos-busqueda-matrona.html?recientes=true",
            # "https://www.laborum.cl/empleos-busqueda-matrones.html?recientes=true",
            # "https://www.laborum.cl/empleos-busqueda-nutricionista.html?recientes=true",
            # "https://www.laborum.cl/empleos-busqueda-paramedico.html?recientes=true"

        ]


#   Then, we rescue the individual values from the list start_urls and scan
#   every website. When we want to scan via a proxy, we use proxy_url. When not, 
#   we use original url.
        for url in self.start_urls:
            if PROXY_LABORUM == "ON":
                source_url = url
                url = self.create_proxy_link(source_url)
            else:
                source_url = url
            yield scrapy.Request(url=url,
                                 cb_kwargs={'source_url':source_url},
                                 meta={
                                    'playwright': True,
                                    'playwright_include_page': True,
                                    'playwright_page_methods': [
                                        PageMethod("wait_for_load_state", "networkidle"),
                                    ]
                                },
                                headers=headers,
                                errback = self.errback_close_page,)

   

    def parse(self, response, source_url):

        page = response.meta["playwright_page"]

#       We log the open of the spider.        
        self.log_init(source_url)

#       We search for the root selector to work with
        root = response.css('div#listado-avisos').xpath('*')

        if not root:
            handle_parsing_error(self, None, self.posting_service, "DOMError")

        for job_offer in root: 
            item = LaborumItemLoader(selector=job_offer)

            item.add_xpath('title', './/h3/text()')
            item.add_value('source_url', source_url)
            item.add_xpath('posting_url', './/a/@href')
            item.add_xpath('company', './/h3/text()')
            
            print(item._local_values)
            
            # item.add_xpath('published_date', './/p/text()', Compose(lambda v: v[-2]))

            
            # if not job_offer.xpath('.//p/a/text()'):
                
            #     item.add_xpath('geolocalization', './/p/span/text()') 
            # else:
            #     item.add_xpath('company', './/p/a/text()')
            #     item.add_xpath('geolocalization','.//p/span/text()', MapCompose(lambda v: "".join(v)))

            # if job_offer.xpath('.//div/span/text()').get() == "Se precisa Urgente":
            #     item.add_value('urgency_required', True)

            item.add_value('posting_service', self.posting_service)
            
            yield item.load_item()

        self.log_finish(source_url)


            

    async def errback_close_page(self, failure):
        page = failure.request.meta["playwright_page"]
        handle_parsing_error(self, failure, self.posting_service, "OtherError", None)
        
        await page.close()
    