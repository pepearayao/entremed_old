import schedule
import time
from constants import *
from functions import *
from errorhandling import *

def schedule_chiletrabajo():

    os.environ["JWT"] = get_watchdog_api_jwt()
#   We send the request to Scrapyd.
    response = post_new_spider_job('entremed', 'cltrablisting')

#   We log the spider created and if there is an invalid response or a status
#   code different from 200, we log an error.
    if check_response(response):
        response = post_log_spider_job(response["response"].json()["jobid"],
                            response["response"].json()["status"],
                            'cltrablisting',
                            'Chiletrabajo')
        if check_response(response):
            return

    handle_error(response)
    return

time.sleep(5)
try:
    schedule.every(30).minutes.do(schedule_chiletrabajo)

    while True:
        schedule.run_pending()
        time.sleep(1)
except:
    send_emergency_telegram()
