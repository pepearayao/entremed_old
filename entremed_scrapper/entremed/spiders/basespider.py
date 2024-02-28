import scrapy
from datetime import datetime, timezone
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError


class BaseSpider(scrapy.Spider):

    def log_init(self,url):

        now = datetime.now(timezone.utc)
        time_now = now.strftime("%H:%M:%S")
        self.logger.info(f"{time_now} Started reading site: {url}")
        return

    def log_finish(self,url):

        now = datetime.now(timezone.utc)
        time_now = now.strftime("%H:%M:%S")
        self.logger.info(f"{time_now} Finished reading site: {url}")
        return

    def save_error_on_db(self, url, web_service, error_type, failure):

        return

    def log_scrapping_error(self, failure, web_service):

        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error(f'HttpError on {response.url}')
            self.save_error_on_db(response.url, web_service, "HttpError", failure)
        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error(f'DNSLookupError on {request.url}')
            self.save_error_on_db(request.url, web_service, "DNSLookupError", failure)
        elif failure.check(TimeoutError):
            request = failure.request
            self.logger.error(f'TimeoutError on {request.url}')
            self.save_error_on_db(request.url, web_service, "TimeoutError", failure)

        return

    def log_dom_reading_error(self, url, web_service):

        self.logger.error(f'DOM reading error on {web_service} site on url {url}')
        self.save_error_on_db(url, web_service, "DomChanged", None)

        return
