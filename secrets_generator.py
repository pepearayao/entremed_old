from secrets import token_bytes
from base64 import b64encode
import sys
import subprocess

dict_to_secret = {
    'jobs_db_name': 'entremed',
    'jobs_db_username': 'user_' + str(b64encode(token_bytes(8)).decode()),
    'jobs_db_password': b64encode(token_bytes(64)).decode(),
    'watchdog_db_name': 'watchdog',
    'watchdog_db_username': 'user_' + str(b64encode(token_bytes(8)).decode()),
    'watchdog_db_password': b64encode(token_bytes(64)).decode(),
    'raw_jobs_api_username':  'raw_jobs_' + str(b64encode(token_bytes(8)).decode()),
    'raw_jobs_api_password':  b64encode(token_bytes(64)).decode(),
    'scrapper_api_username':  'scrapyd',
    'scrapper_api_password':  '474c7419e9febbccaecb466e8e231abe0fc219d0c75db73c46859c7670b87716',
    'watchdog_api_username':  'watchdog_' + str(b64encode(token_bytes(8)).decode()),
    'watchdog_api_password':  b64encode(token_bytes(64)).decode(),
}

dict_to_secret['telegram_bot_token'] = str(input('Please enter the telegram token for the bot.'))
dict_to_secret['telegram_alert_channel'] = str(input('Please enter the telegram channel to which we alert.'))


print('Will generate and display codes only one time here. Starting...')

for key,value in dict_to_secret.items():
    result = subprocess.run(
        [f"echo {value} | docker secret create {key} -"],
        shell=True,
        capture_output=True,
        text=True)
    if result.returncode != 0:
        sys.exit('Error: Maybe you havent initiated as a Swarm?')

    print(f'Secret for {key} generated sucessfully. Value: {value}')
