import requests
import socket
from datetime import datetime, timezone
import json
from entremed.constants import *
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError



def send_emergency_telegram():
    
    message = f"MENSAJE DE MÁXIMA CRITICIDAD.\nEl container <<Scrapper>> lanzó un error grave y dejó de scrappear. Probablemente las API no estén respondiendo." 
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={TELEGRAM_ALERT_CHANNEL_ID}&text={message}" 
    requests.get(url)

def send_error(error:dict):
    data = json.dumps(error, default=str) + "\n"
    try:
        response = requests.request("POST",
                                    WATCHDOG_LOGS_ERRORS_REQUEST_URL,
                                    data=data
                                    )
        print(response._content)
        if response.status_code != 201:
            send_emergency_telegram()
    except:
        send_emergency_telegram()
    
    return

def handle_error(response:str,spider):

    payload = {'docker_name': 'Scrapper',
               'process_name': spider.name,
               'service_ip': socket.gethostbyname_ex(socket.getfqdn())[2][0],
               'creation_time': datetime.now(timezone.utc)
               }

    if response["response_type"] == 'invalid':
        payload["error_type"] = 'ConnectionError'
        payload["error_detail"] = response["body"]

    
    else: 
        payload["error_type"] = 'HTTPError'
        payload["http_status_code"] = response["response"].status_code
        payload["error_detail"] = response["response"].json()["detail"]
    
    send_error(payload)

    return

def handle_parsing_error(spider, failure, web_service, error_type, source_url):

    payload = {'docker_name': 'Scrapper',
               'process_name': spider.name,
               'service_ip': socket.gethostbyname_ex(socket.getfqdn())[2][0],
               'creation_time': datetime.now(timezone.utc)
               }
    if error_type == 'DOMError':
        payload["error_type"] = 'DOMError'
        payload["error_detail"] = "No content"
        payload["website_error"] = source_url
        payload["posting_service"] = web_service
    else:
        if failure.check(DNSLookupError):
            request = failure.request
            payload["error_type"] = 'DNSLookupError'
            payload["error_detail"] = failure
            payload["website_error"] = request.url
            payload["posting_service"] = web_service
            
        elif failure.check(TimeoutError):
            request = failure.request
            payload["error_type"] = 'TimeoutError'
            payload["error_detail"] = failure
            payload["website_error"] = request.url
            payload["posting_service"] = web_service
        
        else:
            request = failure.request
            payload["error_type"] = 'HttpError'
            payload["error_detail"] = failure
            payload["website_error"] = request.url
            payload["posting_service"] = web_service

    send_error(payload)