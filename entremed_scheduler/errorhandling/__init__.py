import socket 
import json
import requests
from datetime import datetime, timezone
from constants import *

def send_emergency_telegram():
    message = f"MENSAJE DE MÁXIMA CRITICIDAD.\nEl container <<Scheduler>> lanzó un error grave y se bajó. Probablemente las APIs no estén respondiendo." 
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={TELEGRAM_ALERT_CHANNEL_ID}&text={message}" 
    requests.get(url)


def send_error(error:dict):
    data = json.dumps(error, default=str) + "\n"
    response = requests.request("POST",
                                    WATCHDOG_LOGS_ERRORS_REQUEST_URL,
                                    data=data
                                    )
    try:
        if response.status_code != 201:
            send_emergency_telegram()
    except:
        send_emergency_telegram()
    
    return


def handle_error(response:str):
#   Nombre del Docker
#   Nombre del Proceso
#   IP
#   Tipo de error (ConnectionError, HTTPError, DNSError, DOMError, SpiderExceptionError, ResourcesError)
#   HTTP Status Code
#   Error detail
    
    payload = {'docker_name': 'Scheduler',
               'process_name': 'Scheduler',
               'service_ip': socket.gethostbyname_ex(socket.getfqdn())[2][0],
               'creation_time': datetime.now(timezone.utc)
               }

    if response["response_type"] == 'invalid':
        payload["error_type"] = 'ConnectionError'
        payload["error_detail"] = response["body"]
        send_error(payload)
    
    else: 
        payload["error_type"] = 'HTTPError'
        payload["http_status_code"] = response["response"].status_code
        payload["error_detail"] = response["response"].json()["detail"]
        send_error(payload)

    print(payload)