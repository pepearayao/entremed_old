import scrapy
from entremed.items import CompuTrabItemLoader
from .basespider import * 
from entremed.constants import *
from entremed.global_functions import handle_parsing_error
from itemloaders.processors import MapCompose, Compose

class ComputrablistingSpider(BaseSpider):
    name = "computrablisting"
    allowed_domains = ["www.computrabajo.cl"]

#   We define the name of the Webservice worked here.
    posting_service = "Computrabajo"

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
            "https://www.computrabajo.cl/trabajo-de-tens-en-rmetropolitana?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-tens-en-valparaiso?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-tens-en-biobio?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-tens-en-antofagasta?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-tens-en-los-lagos?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-tens-en-libertador-b-o-higgins?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-tens-en-maule?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-tens-en-coquimbo?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-tens-en-araucania?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-tens-en-atacama?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-tens-en-tarapaca?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-tens-en-los-rios?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-tens-en-magallanes-y-antartica-chilena?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-enfermera-en-rmetropolitana?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-enfermera-en-valparaiso?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-enfermera-en-biobio?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-enfermera-en-antofagasta?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-enfermera-en-los-lagos?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-enfermera-en-libertador-b-o-higgins?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-enfermera-en-maule?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-enfermera-en-coquimbo?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-enfermera-en-araucania?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-enfermera-en-atacama?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-enfermera-en-tarapaca?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-enfermera-en-los-rios?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-enfermera-en-magallanes-y-antartica-chilena?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-psicologo-en-rmetropolitana?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-psicologo-en-valparaiso?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-psicologo-en-biobio?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-psicologo-en-antofagasta?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-psicologo-en-los-lagos?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-psicologo-en-libertador-b-o-higgins?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-psicologo-en-maule?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-psicologo-en-coquimbo?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-psicologo-en-araucania?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-psicologo-en-atacama?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-psicologo-en-tarapaca?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-psicologo-en-los-rios?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-psicologo-en-magallanes-y-antartica-chilena?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-kinesiologo-en-rmetropolitana?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-kinesiologo-en-valparaiso?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-kinesiologo-en-biobio?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-kinesiologo-en-antofagasta?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-kinesiologo-en-los-lagos?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-kinesiologo-en-libertador-b-o-higgins?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-kinesiologo-en-maule?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-kinesiologo-en-coquimbo?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-kinesiologo-en-araucania?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-kinesiologo-en-atacama?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-kinesiologo-en-tarapaca?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-kinesiologo-en-los-rios?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-kinesiologo-en-magallanes-y-antartica-chilena?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-odontologo-en-rmetropolitana?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-odontologo-en-valparaiso?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-odontologo-en-biobio?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-odontologo-en-antofagasta?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-odontologo-en-los-lagos?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-odontologo-en-libertador-b-o-higgins?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-odontologo-en-maule?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-odontologo-en-coquimbo?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-odontologo-en-araucania?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-odontologo-en-atacama?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-odontologo-en-tarapaca?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-odontologo-en-los-rios?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-odontologo-en-magallanes-y-antartica-chilena?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-psicopedagogo-en-rmetropolitana?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-psicopedagogo-en-valparaiso?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-psicopedagogo-en-biobio?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-psicopedagogo-en-antofagasta?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-psicopedagogo-en-los-lagos?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-psicopedagogo-en-libertador-b-o-higgins?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-psicopedagogo-en-maule?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-psicopedagogo-en-coquimbo?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-psicopedagogo-en-araucania?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-psicopedagogo-en-atacama?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-psicopedagogo-en-tarapaca?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-psicopedagogo-en-los-rios?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-psicopedagogo-en-magallanes-y-antartica-chilena?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-fonoaudiologo-en-rmetropolitana?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-fonoaudiologo-en-valparaiso?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-fonoaudiologo-en-biobio?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-fonoaudiologo-en-antofagasta?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-fonoaudiologo-en-los-lagos?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-fonoaudiologo-en-libertador-b-o-higgins?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-fonoaudiologo-en-maule?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-fonoaudiologo-en-coquimbo?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-fonoaudiologo-en-araucania?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-fonoaudiologo-en-atacama?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-fonoaudiologo-en-tarapaca?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-fonoaudiologo-en-los-rios?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-fonoaudiologo-en-magallanes-y-antartica-chilena?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-nutricionista-en-rmetropolitana?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-nutricionista-en-valparaiso?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-nutricionista-en-biobio?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-nutricionista-en-antofagasta?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-nutricionista-en-los-lagos?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-nutricionista-en-libertador-b-o-higgins?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-nutricionista-en-maule?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-nutricionista-en-coquimbo?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-nutricionista-en-araucania?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-nutricionista-en-atacama?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-nutricionista-en-tarapaca?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-nutricionista-en-los-rios?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-nutricionista-en-magallanes-y-antartica-chilena?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-paramedico-en-rmetropolitana?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-paramedico-en-valparaiso?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-paramedico-en-biobio?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-paramedico-en-antofagasta?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-paramedico-en-los-lagos?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-paramedico-en-libertador-b-o-higgins?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-paramedico-en-maule?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-paramedico-en-coquimbo?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-paramedico-en-araucania?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-paramedico-en-atacama?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-paramedico-en-tarapaca?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-paramedico-en-los-rios?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-paramedico-en-magallanes-y-antartica-chilena?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-matrona-en-rmetropolitana?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-matrona-en-valparaiso?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-matrona-en-biobio?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-matrona-en-antofagasta?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-matrona-en-los-lagos?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-matrona-en-libertador-b-o-higgins?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-matrona-en-maule?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-matrona-en-coquimbo?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-matrona-en-araucania?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-matrona-en-atacama?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-matrona-en-tarapaca?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-matrona-en-los-rios?by=publicationtime",
            "https://www.computrabajo.cl/trabajo-de-matrona-en-magallanes-y-antartica-chilena?by=publicationtime"
        ]


#   Then, we rescue the individual values from the list start_urls and scan
#   every website. When we want to scan via a proxy, we use proxy_url. When not, 
#   we use original url.
        for url in self.start_urls:
            if PROXY_COMPUTRABAJO == "ON":
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
        root = response.css('article.box_offer')
        if not root:
            handle_parsing_error(self, None, self.posting_service, "DOMError")

        for job_offer in root: 
            item = CompuTrabItemLoader(selector=job_offer)

            item.add_xpath('title', './/h2/a/text()')
            item.add_value('source_url', source_url)
            item.add_xpath('posting_url', './/h2/a/@href')
            item.add_xpath('published_date', './/p/text()', Compose(lambda v: v[-2]))

            
            if not job_offer.xpath('.//p/a/text()'):
                item.add_xpath('company', './/p/text()')
                item.add_xpath('geolocalization', './/p/span/text()') 
            else:
                item.add_xpath('company', './/p/a/text()')
                item.add_xpath('geolocalization','.//p/span/text()', MapCompose(lambda v: "".join(v)))

            if job_offer.xpath('.//div/span/text()').get() == "Se precisa Urgente":
                item.add_value('urgency_required', True)

            item.add_value('posting_service', self.posting_service)
            
            yield item.load_item()

        self.log_finish(source_url)


            

    async def errback_close_page(self, failure):
        handle_parsing_error(self, failure, self.posting_service, "OtherError", None)
        return
    