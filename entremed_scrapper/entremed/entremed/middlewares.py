# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from entremed.global_functions import get_jwt, save_job_postings, schedule_job_posting, update_self_log, update_job_posting
from entremed.error_handling import *

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import re

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
        spider.raw_jobs_jwt = get_jwt('rawjobs')
        spider.watchdog_jwt = get_jwt('watchdog')
        spider.jobpostings = []
        spider.nextscrappings = []
        spider.detailed_scan = None

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
        job_id = spider.settings["LOG_FILE"].split("/")[-1].split(".")[0] if spider.settings["LOG_FILE"] != None else "ManualSpiderRun"

        if re.search(r"listing",spider.name):
        # We send the Job Posting to the API to be saved
            if save_job_postings(spider):
        # We schedule the scrape of these new job postings and inform watchdog
                if schedule_job_posting(spider):
        # Then, after all, we close the spider and report to watchdog.
                    update_self_log(spider, True, stats, job_id)
                    return
                else:
                    update_self_log(spider, False, stats, job_id)
                    return

        elif re.search(r"post",spider.name):
            if update_job_posting(spider):
                update_self_log(spider,True,stats,job_id)
                return
            else:
                update_self_log(spider,False,stats,job_id)
                return
