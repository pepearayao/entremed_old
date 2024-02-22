from entremed.error_handling import *

def put_request(request_url:str, headers:str, data:str):
    #   We try to send the request. If it fails we send the error type name.
    try:
        response = requests.request("PUT",
                                    request_url,
                                    data=data,
                                    headers=headers
                                    )
        return {'response_type': 'valid', 'response': response}
    
    except Exception as e:
        return {'response_type': 'invalid', 'response': type(e).__name__, 'body': e} 

def post_request(request_url:str, headers:str, data:str, auth:str):
#   We try to send the request. If it fails we send the error type name.
    try:
        response = requests.request("POST",
                                    request_url,
                                    data=data,
                                    headers=headers,
                                    auth=auth)
        return {'response_type': 'valid', 'response': response}
    
    except Exception as e:
        return {'response_type': 'invalid', 'response': type(e).__name__, 'body': e} 

def check_response(response):
    if response["response_type"] == 'valid':
        if response["response"].ok or response["response"].status_code == 409:
            return True
        
    return False

def get_jwt(service):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}
    if service == 'rawjobs':
        request_url = RAW_JOBS_AUTH_REQUEST_URL
        payload = {'username': RAW_JOBS_API_USERNAME, 'password': RAW_JOBS_API_PASSWORD}
    elif service == 'watchdog':
        request_url = WATCHDOG_AUTH_REQUEST_URL
        payload = {'username': WATCHDOG_API_USERNAME, 'password': WATCHDOG_API_PASSWORD}
    
    response = post_request(request_url, headers,payload, None)
    
    if check_response(response):
        return response["response"].json()["access_token"]
    else:
        handle_error(response)
        return 

def save_job_postings(spider):
    # We get the JWT first created at the beggining of the spider. Then, we
    # save each job offer one by one. When it is saved, we save that info of 
    # the new entry into a list. 
        headers = {'Authorization': f'Bearer {spider.raw_jobs_jwt}'}
        for item in spider.jobpostings:
            data = json.dumps(item.asdict(), default=str) + "\n"
            
            response = post_request(RAW_JOBS_REQUEST_URL,headers,data,None)

            if check_response(response):
                if response["response"].ok:
                    spider.nextscrappings.\
                            append({'id': response["response"].json()["new_entry_id"],
                                'posting_url': item["posting_url"],
                                'posting_service': item["posting_service"]})
            else:
                handle_error(response,spider)
                return False
        return True
   
def schedule_job_posting(spider):
    # We schedule to run Scrapyd for each new item saved. Then after each 
    # scheduled spider, we store status in watchdog.
        for item in spider.nextscrappings:
    
    # First we send the request to Scrapyd to schedule new scrappings.
            payload = {'project':'entremed',
                        'spider':MAPPING_DICT[item["posting_service"]],
                        'id': item['id'], 
                        'url':item["posting_url"]}
            auth = (SCRAPYD_API_USERNAME, SCRAPYD_API_PASSWORD)
            
            response = post_request(SCRAPYD_REQUEST_URL,None,payload,auth)

            if check_response(response):
                create_new_log(spider, response, item)
            else:
                handle_error(response,spider)
                return False
        spider.crawler.stats.set_value('items_saved', len(spider.nextscrappings))
        return True

def create_new_log(spider, response, item):
    
    payload = {'job_id': response["response"].json()["jobid"],
                'scheduled_status': response["response"].json()["status"],
                'spider_name': MAPPING_DICT[item["posting_service"]],
                'posting_service': item["posting_service"]}
    payload = json.dumps(payload, default=str) + "\n"
    
    headers = {'Authorization': f'Bearer {spider.watchdog_jwt}'}
    
    response = post_request(WATCHDOG_LOGS_SPIDERS_REQUEST_URL,headers,payload,None)

    if check_response(response):
        return
    else:
        handle_error(response,spider) 

def update_self_log(spider, condition, stats, job_id):
    
    if condition:
        scheduled_status = 'finished'
        exit_status = stats["finish_reason"]
        start_time = stats["start_time"]
        memusage_startup = stats["memusage/startup"]
        memusage_max = stats["memusage/max"]
        elapsed_time_seconds = stats["elapsed_time_seconds"]
        finish_time = stats["finish_time"]
        items_scraped = stats["item_scraped_count"]
        items_saved = stats["items_saved"]
        payload = {'job_id': job_id,
                    'scheduled_status': scheduled_status,
                    'exit_status': exit_status,
                    'start_time': start_time,
                    'memusage_startup': memusage_startup,
                    'memusage_max': memusage_max,
                    'elapsed_time_seconds': elapsed_time_seconds,
                    'end_time': finish_time,
                    'items_scraped': items_scraped,
                    'items_saved': items_saved}
    else:  
        payload = {'scheduled_status': 'finished', 'exit_status': 'failed',}
    
    payload = json.dumps(payload, default=str) + "\n"
    headers = {'Authorization': f'Bearer {spider.watchdog_jwt}'}
    
    response = put_request(WATCHDOG_LOGS_SPIDERS_REQUEST_URL + "/" + job_id, headers, payload)

    if check_response(response):
        return
    else:
        handle_error(response,spider)

def update_job_posting(spider):
    # We get the JWT first created at the beggining of the spider. Then, we
    # save the detailed job offer.
 
        headers = {'Authorization': f'Bearer {spider.raw_jobs_jwt}'}
        adapter = spider.detailed_scan
        data = json.dumps(adapter.asdict(), default=str) + "\n"
        response = put_request(RAW_JOBS_REQUEST_URL + f"/{spider.id}",headers,data)
        spider.crawler.stats.set_value('items_saved', "0")
        
        if check_response(response):
            if response["response"].ok:
                return True 
        else:
            handle_error(response,spider)
            return False