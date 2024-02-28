import os

# SCRAPY API ACCESS DATA VARIABLES
SCRAPYD_API_ROOT_URL = os.environ["SCRAPYD_API_ROOT_URL"]
SCRAPYD_API_PORT = os.environ["SCRAPYD_API_PORT"]
SCRAPYD_API_SCHEDULE_EXTENSION = os.environ["SCRAPYD_API_SCHEDULE_EXTENSION"]
SCRAPYD_API_USERNAME = (open("/run/secrets/scrapper_api_username", "r").read()).strip()
SCRAPYD_API_PASSWORD = (open("/run/secrets/scrapper_api_password", "r").read()).strip()

# WATCHDOG API ACCESS DATA VARIABLES
WATCHDOG_API_ROOT_URL = os.environ["WATCHDOG_API_ROOT_URL"]
WATCHDOG_API_PORT = os.environ["WATCHDOG_API_PORT"]
WATCHDOG_API_LOGS_SPIDERS_EXTENSION = os.environ["WATCHDOG_API_LOGS_SPIDERS_EXTENSION"]
WATCHDOG_API_LOGS_ERRORS_EXTENSION = os.environ["WATCHDOG_API_LOGS_ERRORS_EXTENSION"]
WATCHDOG_API_LOGS_MESSAGES_EXTENSION = os.environ["WATCHDOG_API_LOGS_MESSAGES_EXTENSION"]
WATCHDOG_API_AUTH_EXTENSION = os.environ["WATCHDOG_API_AUTH_EXTENSION"]
WATCHDOG_API_USERNAME = (open("/run/secrets/watchdog_api_username", "r").read()).strip()
WATCHDOG_API_PASSWORD = (open("/run/secrets/watchdog_api_password", "r").read()).strip()

# RAW_JOBS API ACCESS DATA VARIABLES
RAW_JOBS_API_ROOT_URL = os.environ["RAW_JOBS_API_ROOT_URL"]
RAW_JOBS_API_PORT = os.environ["RAW_JOBS_API_PORT"]
RAW_JOBS_API_JOBS_EXTENSION = os.environ["RAW_JOBS_API_JOBS_EXTENSION"]
RAW_JOBS_API_AUTH_EXTENSION = os.environ["RAW_JOBS_API_AUTH_EXTENSION"]
RAW_JOBS_API_USERNAME = (open("/run/secrets/raw_jobs_api_username", "r").read()).strip()
RAW_JOBS_API_PASSWORD = (open("/run/secrets/raw_jobs_api_password", "r").read()).strip()

# TELEGRAM API ACCESS KEYS
TELEGRAM_BOT_TOKEN = (open("/run/secrets/telegram_bot_token", "r").read()).strip()
TELEGRAM_ALERT_CHANNEL_ID = (open("/run/secrets/telegram_alert_channel", "r").read()).strip()

# APIS URL CONSTRUCTION
SCRAPYD_REQUEST_URL = SCRAPYD_API_ROOT_URL + ":" + SCRAPYD_API_PORT + SCRAPYD_API_SCHEDULE_EXTENSION

WATCHDOG_LOGS_SPIDERS_REQUEST_URL = WATCHDOG_API_ROOT_URL + ":" + WATCHDOG_API_PORT + WATCHDOG_API_LOGS_SPIDERS_EXTENSION
WATCHDOG_LOGS_ERRORS_REQUEST_URL = WATCHDOG_API_ROOT_URL + ":" + WATCHDOG_API_PORT + WATCHDOG_API_LOGS_ERRORS_EXTENSION
WATCHDOG_LOGS_MESSAGES_REQUEST_URL = WATCHDOG_API_ROOT_URL + ":" + WATCHDOG_API_PORT + WATCHDOG_API_LOGS_MESSAGES_EXTENSION
WATCHDOG_AUTH_REQUEST_URL = WATCHDOG_API_ROOT_URL + ":" + WATCHDOG_API_PORT + WATCHDOG_API_AUTH_EXTENSION + "/token"

RAW_JOBS_AUTH_REQUEST_URL = RAW_JOBS_API_ROOT_URL + ":" + RAW_JOBS_API_PORT + RAW_JOBS_API_AUTH_EXTENSION + "/token"
RAW_JOBS_REQUEST_URL = RAW_JOBS_API_ROOT_URL + ":" + RAW_JOBS_API_PORT + RAW_JOBS_API_JOBS_EXTENSION

# DICTIONARY MAPPING POSTING SITES TO SPIDER NAMES
MAPPING_DICT = {'Chiletrabajo': 'cltrabpost',
                'Computrabajo': 'computrabpost',
                'Estado': 'estadopost',
                'BNE': 'bnepost',
                'Laborum': 'laborumpost',
                'Serpaj': 'serpajpost',
                'Trabajando': 'trabpost'}

PROXY_CHILETRABAJO = "OFF"
PROXY_COMPUTRABAJO = "OFF"
PROXY_LABORUM = "OFF"