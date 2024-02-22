# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import os
import json
import requests
import re
import settings

def save_job_posting(spider):
    # We get the JWT first created at the beggining of the spider. Then, we
    # save each job offer one by one. When it is saved, we save that info of 
    # the new entry into a list. 
        headers = {'Authorization': f'Bearer {spider.raw_jobs_jwt}'}
        for item in spider.jobposting:
            data_line = json.dumps(item.asdict(), default=str) + "\n"
            response = requests.request("POST", 
                                        settings.RAW_JOBS_REQUEST_URL, 
                                        headers=headers, 
                                        data=data_line)
            if response.status_code == 201:
                spider.nextscrappings.\
                append({'id': response.json()["new_entry_id"],
                        'posting_url': item["posting_url"],
                        'posting_service': item["posting_service"]})
            elif response.status_code == 409:
                continue
            else:
                #MANDAR ERROR A WATCHDOG
                pass
    
def schedule_job_posting(spider):
    # We schedule to run Scrapyd for each new item saved. Then after each 
    # scheduled spider, we store status in watchdog.
        for item in spider.nextscrappings:
    
    # First we send the request to Scrapyd to schedule new scrappings.
            payload = {'project':'entremed',
                        'spider':settings.MAPPING_DICT[item["posting_service"]],
                        'id': item['id'], 
                        'url':item["posting_url"]}
            auth = (settings.SCRAPYD_API_USERNAME, settings.SCRAPYD_API_PASSWORD)
            
            response = requests.request("POST",
                                        settings.SCRAPYD_REQUEST_URL,
                                        data=payload,
                                        auth=auth)
            
            if response.status_code == 200:
    # Then we send the request to save the Job in the Watchdog.
                create_new_log(spider, response, item)
            
            else:
                send_error_to_watchdog()

def create_new_log(spider, response, item):
    
    payload = {'job_id': response.json()["jobid"],
                'scheduled_status': response.json()["status"],
                'spider_name': spider.name,
                'posting_service': item["posting_service"]}
    
    headers = {'Authorization': f'Bearer {spider.watchdog_jwt}'}
    
    response = requests.request("POST",
                                settings.WATCHDOG_LOGS_SPIDERS_REQUEST_URL,
                                headers=headers,
                                payload=payload)
    
    if response.json()["status"] != 'ok':
        send_error_to_watchdog()

def update_self_log(spider):
    stats = spider.crawler.stats.get_stats()
    spider.logger.info(stats)

def send_error_to_watchdog():
    pass

class EntremedSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
        spider.logger.info(spider.settings["LOG_FILE"])
        

    def spider_closed(self, spider):

        if re.search(r"listing",spider.name):
        
        # We send the Job Posting to the API to be saved
            save_job_posting(spider)

        # We schedule the scrape of these new job postings and inform watchdog
            schedule_job_posting(spider)
        
        # Then, after all, we close the spider and report to watchdog. 
            update_self_log(spider)

        elif re.search(r"post",spider.name):
            pass


        


class EntremedDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class SaveJobStatsMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s
    
    def spider_closed(self, spider, reason):
        stats = spider.crawler.stats.get_stats()
        spider.logger.info(stats)