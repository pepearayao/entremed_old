import os

#SCRAPY API ACCESS DATA VARIABLES
SCRAPYD_API_ROOT_URL = os.environ["SCRAPYD_API_ROOT_URL"]
SCRAPYD_API_PORT = os.environ["SCRAPYD_API_PORT"]
SCRAPYD_API_USERNAME = (open("/run/secrets/scrapper_api_username", "r").read()).strip()
SCRAPYD_API_PASSWORD = (open("/run/secrets/scrapper_api_password", "r").read()).strip()
SCRAPYD_API_SCHEDULE_EXTENSION = os.environ["SCRAPYD_API_SCHEDULE_EXTENSION"]

#WATCHDOG API ACCESS DATA VARIABLES
WATCHDOG_API_ROOT_URL = os.environ["WATCHDOG_API_ROOT_URL"]
WATCHDOG_API_PORT = os.environ["WATCHDOG_API_PORT"]
WATCHDOG_API_USERNAME = (open("/run/secrets/watchdog_api_username", "r").read()).strip()
WATCHDOG_API_PASSWORD = (open("/run/secrets/watchdog_api_password", "r").read()).strip()

WATCHDOG_API_LOGS_SPIDERS_EXTENSION = os.environ["WATCHDOG_API_LOGS_SPIDERS_EXTENSION"]
WATCHDOG_API_LOGS_ERRORS_EXTENSION = os.environ["WATCHDOG_API_LOGS_ERRORS_EXTENSION"]
WATCHDOG_API_LOGS_MESSAGES_EXTENSION = os.environ["WATCHDOG_API_LOGS_MESSAGES_EXTENSION"]

WATCHDOG_API_AUTH_EXTENSION = os.environ["WATCHDOG_API_AUTH_EXTENSION"]

# TELEGRAM API ACCESS KEYS
TELEGRAM_BOT_TOKEN = (open("/run/secrets/telegram_bot_token", "r").read()).strip()
TELEGRAM_ALERT_CHANNEL_ID = (open("/run/secrets/telegram_alert_channel", "r").read()).strip()

# APIS URL CONSTRUCTION
SCRAPYD_REQUEST_URL = SCRAPYD_API_ROOT_URL + ":" + SCRAPYD_API_PORT + SCRAPYD_API_SCHEDULE_EXTENSION

WATCHDOG_LOGS_SPIDERS_REQUEST_URL = WATCHDOG_API_ROOT_URL + ":" + WATCHDOG_API_PORT + WATCHDOG_API_LOGS_SPIDERS_EXTENSION
WATCHDOG_LOGS_ERRORS_REQUEST_URL = WATCHDOG_API_ROOT_URL + ":" + WATCHDOG_API_PORT + WATCHDOG_API_LOGS_ERRORS_EXTENSION
WATCHDOG_LOGS_MESSAGES_REQUEST_URL = WATCHDOG_API_ROOT_URL + ":" + WATCHDOG_API_PORT + WATCHDOG_API_LOGS_MESSAGES_EXTENSION
WATCHDOG_AUTH_REQUEST_URL = WATCHDOG_API_ROOT_URL + ":" + WATCHDOG_API_PORT + WATCHDOG_API_AUTH_EXTENSION + "/token"
