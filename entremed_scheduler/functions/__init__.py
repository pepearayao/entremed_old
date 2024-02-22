import requests
import json
from constants import *
from errorhandling import *

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

def check_response(response:dict):
    if response["response_type"] == 'valid':
        if response["response"].ok:
            return True
    else:
        return False

def get_watchdog_api_jwt():
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'Accept': 'application/json'}
        payload = {'username': WATCHDOG_API_USERNAME,
                   'password': WATCHDOG_API_PASSWORD}
        response = post_request(WATCHDOG_AUTH_REQUEST_URL,headers,payload,None)
        
        if check_response(response):
            return response["response"].json()["access_token"]
        else:
            handle_error(response)
            return 

def post_new_spider_job(project:str, spider_name:str):

#   We create payload and auth oken for Scrapy Server
    payload = {'project':project, 'spider':spider_name}
    auth = (SCRAPYD_API_USERNAME, SCRAPYD_API_PASSWORD)

    response = post_request(SCRAPYD_REQUEST_URL,None,payload,auth)
    
    return response

def post_log_spider_job(job_id:str, status:str, spider_name:str, posting_service:str):
#   We create the payload and auth to store the new spider jobid in database   
    jwt = os.environ["JWT"]
    
    payload = {'job_id': job_id,
               'scheduled_status': status,
               'spider_name': spider_name,
               'posting_service': posting_service}
    payload = json.dumps(payload, default=str) + "\n"
    headers = {'Authorization': f'Bearer {jwt}'}
    
    response = post_request(WATCHDOG_LOGS_SPIDERS_REQUEST_URL,headers,payload,None)

    return response

