import scrapy
from entremed.items import ClTrabItemLoader
from .basespider import *
from entremed.constants import *
from entremed.global_functions import handle_parsing_error

class CltrablistingSpider(BaseSpider):
    name = "cltrablisting"
    allowed_domains = ["www.chiletrabajos.cl"]

#   We define the name of the Webservice worked here.
    posting_service = "Chiletrabajo"

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
            "https://www.chiletrabajos.cl/encuentra-un-empleo?2=enfermera&13=&fecha=3&categoria=&8=&14=&inclusion=&f=2"
            "https://www.chiletrabajos.cl/encuentra-un-empleo?2=enfermeria&13=&fecha=3&categoria=&8=&14=&inclusion=&f=2",
            "https://www.chiletrabajos.cl/encuentra-un-empleo?2=tens&13=&fecha=3&categoria=&8=&14=&inclusion=&f=2",
            "https://www.chiletrabajos.cl/encuentra-un-empleo?2=tecnico+en+enfermeria&13=&fecha=3&categoria=&8=&14=&inclusion=&f=2",
            "https://www.chiletrabajos.cl/encuentra-un-empleo?2=psicologo&13=&fecha=3&categoria=&8=&14=&inclusion=&f=2",
            "https://www.chiletrabajos.cl/encuentra-un-empleo?2=psicologia&13=&fecha=3&categoria=&8=&14=&inclusion=&f=2",
            "https://www.chiletrabajos.cl/encuentra-un-empleo?2=odontologo&13=&fecha=3&categoria=&8=&14=&inclusion=&f=2",
            "https://www.chiletrabajos.cl/encuentra-un-empleo?2=odontologia&13=&fecha=3&categoria=&8=&14=&inclusion=&f=2",
            "https://www.chiletrabajos.cl/encuentra-un-empleo?2=kinesiologo&13=&fecha=3&categoria=&8=&14=&inclusion=&f=2",
            "https://www.chiletrabajos.cl/encuentra-un-empleo?2=kinesiologia&13=&fecha=3&categoria=&8=&14=&inclusion=&f=2",
            "https://www.chiletrabajos.cl/encuentra-un-empleo?2=psicopedagogo&13=&fecha=3&categoria=&8=&14=&inclusion=&f=2",
            "https://www.chiletrabajos.cl/encuentra-un-empleo?2=psicopedagogia&13=&fecha=3&categoria=&8=&14=&inclusion=&f=2",
            "https://www.chiletrabajos.cl/encuentra-un-empleo?2=fonoaudiologo&13=&fecha=3&categoria=&8=&14=&inclusion=&f=2",
            "https://www.chiletrabajos.cl/encuentra-un-empleo?2=fonoaudiologia&13=&fecha=3&categoria=&8=&14=&inclusion=&f=2",
            "https://www.chiletrabajos.cl/encuentra-un-empleo?2=nutricionista&13=&fecha=3&categoria=&8=&14=&inclusion=&f=2",
            "https://www.chiletrabajos.cl/encuentra-un-empleo?2=paramedico&13=&fecha=3&categoria=&8=&14=&inclusion=&f=2"
        ]

#   Then, we rescue the individual values from the list start_urls and scan
#   every website. When we want to scan via a proxy, we use proxy_url. When not,
#   we use original url.
        for url in self.start_urls:
            if PROXY_CHILETRABAJO == "ON":
                source_url = url
                url = self.create_proxy_link(source_url)
            else:
                source_url = url
            yield scrapy.Request(url,
                                 headers=headers,
                                 cb_kwargs={'source_url':source_url},
                                 errback = self.errback_close_page,)



    def parse(self, response, source_url):

#       We log the open of the spider.
        self.log_init(source_url)

#       We search for the root selector to work with
        root = response.css('div.job-item')

        if not root:
            handle_parsing_error(self, None, self.posting_service, "DOMError",source_url)

        for job_offer in root:
            item = ClTrabItemLoader(selector=job_offer)

            item.add_xpath('title', './/*[1]/h2/a/text()')
            item.add_value('source_url', source_url)
            item.add_xpath('posting_url', './/*[1]/h2/a/@href')
            item.add_xpath('company', './/*[1]/*[3]/text()')
            item.add_xpath('geolocalization', './/*[1]/*[3]/a/text()')
            item.add_xpath('inclusive_posting',
                           './/div/div/a[@title="Elegible ley de inclusion"]')
            item.add_value('posting_service', self.posting_service)

            yield item.load_item()

        self.log_finish(source_url)




    async def errback_close_page(self, failure):
        handle_parsing_error(self, failure, self.posting_service, "OtherError", None)
        return
