import scrapy
from datetime import datetime, timezone
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError
import requests
import os

# SCRAPY API ACCESS DATA VARIABLES
SCRAPYD_API_ROOT_URL = os.environ["SCRAPYD_API_ROOT_URL"]
SCRAPYD_API_PORT = os.environ["SCRAPYD_API_PORT"]
SCRAPYD_API_USERNAME = os.environ["SCRAPYD_API_USERNAME"]
SCRAPYD_API_PASSWORD = os.environ["SCRAPYD_API_PASSWORD"]
SCRAPYD_API_SCHEDULE_EXTENSION = os.environ["SCRAPYD_API_SCHEDULE_EXTENSION"]

# WATCHDOG API ACCESS DATA VARIABLES
WATCHDOG_API_ROOT_URL = os.environ["WATCHDOG_API_ROOT_URL"]
WATCHDOG_API_PORT = os.environ["WATCHDOG_API_PORT"]
WATCHDOG_API_USERNAME = os.environ["WATCHDOG_API_USERNAME"]
WATCHDOG_API_PASSWORD = os.environ["WATCHDOG_API_PASSWORD"]
WATCHDOG_API_LOGS_SPIDERS_EXTENSION = os.environ["WATCHDOG_API_LOGS_SPIDERS_EXTENSION"]
WATCHDOG_API_LOGS_ERRORS_EXTENSION = os.environ["WATCHDOG_API_LOGS_ERRORS_EXTENSION"]
WATCHDOG_API_LOGS_MESSAGES_EXTENSION = os.environ["WATCHDOG_API_LOGS_MESSAGES_EXTENSION"]
WATCHDOG_API_AUTH_EXTENSION = os.environ["WATCHDOG_API_AUTH_EXTENSION"]

# RAW_JOBS API ACCESS DATA VARIABLES
RAW_JOBS_API_ROOT_URL = os.environ["RAW_JOBS_API_ROOT_URL"]
RAW_JOBS_API_PORT = os.environ["RAW_JOBS_API_PORT"]
RAW_JOBS_API_JOBS_EXTENSION = os.environ["RAW_JOBS_API_JOBS_EXTENSION"]
RAW_JOBS_API_AUTH_EXTENSION = os.environ["RAW_JOBS_API_AUTH_EXTENSION"]
RAW_JOBS_API_USERNAME = os.environ["RAW_JOBS_API_USERNAME"]
RAW_JOBS_API_PASSWORD = os.environ["RAW_JOBS_API_PASSWORD"]


# APIS URL CONSTRUCTION
SCRAPYD_REQUEST_URL = SCRAPYD_API_ROOT_URL + ":" + SCRAPYD_API_PORT + SCRAPYD_API_SCHEDULE_EXTENSION

WATCHDOG_LOGS_SPIDERS_REQUEST_URL = WATCHDOG_API_ROOT_URL + ":" + WATCHDOG_API_PORT + WATCHDOG_API_LOGS_SPIDERS_EXTENSION
WATCHDOG_LOGS_ERRORS_REQUEST_URL = WATCHDOG_API_ROOT_URL + ":" + WATCHDOG_API_PORT + WATCHDOG_API_LOGS_ERRORS_EXTENSION
WATCHDOG_LOGS_MESSAGES_REQUEST_URL = WATCHDOG_API_ROOT_URL + ":" + WATCHDOG_API_PORT + WATCHDOG_API_LOGS_MESSAGES_EXTENSION
WATCHDOG_AUTH_REQUEST_URL = WATCHDOG_API_ROOT_URL + ":" + WATCHDOG_API_PORT + WATCHDOG_API_AUTH_EXTENSION + "/token"

RAW_JOBS_AUTH_REQUEST_URL = RAW_JOBS_API_ROOT_URL + ":" + RAW_JOBS_API_PORT + RAW_JOBS_API_AUTH_EXTENSION + "/token"
RAW_JOBS_REQUEST_URL = RAW_JOBS_API_ROOT_URL + ":" + RAW_JOBS_API_PORT + RAW_JOBS_API_JOBS_EXTENSION

# DICTIONARY MAPPING POSTING SITES TO SPIDER NAMES
MAPPING_DICT = {'Chiletrabajo': 'cltrabpost'}

PROXY_CHILETRABAJO = "OFF"

class BaseSpider(scrapy.Spider):

    def get_jwt(self, service):

        if service == 'rawjobs':
            request_url = RAW_JOBS_AUTH_REQUEST_URL
            headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}
            payload = {'username': RAW_JOBS_API_USERNAME, 'password': RAW_JOBS_API_PASSWORD}
        elif service == 'watchdog':
            request_url = WATCHDOG_AUTH_REQUEST_URL
            headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}
            payload = {'username': WATCHDOG_API_USERNAME, 'password': WATCHDOG_API_PASSWORD}
        response = requests.request("POST", request_url, headers=headers, data=payload)
        if response.status_code == 200:
            return response.json()["access_token"]
        return None
    
    def log_init(self,url):
        
        now = datetime.now(timezone.utc)
        time_now = now.strftime("%H:%M:%S")
        self.logger.info(f"{time_now} Started reading site: {url}")
        return
    
    def log_finish(self,url):
        
        now = datetime.now(timezone.utc)
        time_now = now.strftime("%H:%M:%S")
        self.logger.info(f"{time_now} FInished reading site: {url}")
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