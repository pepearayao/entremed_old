# What is Entremed?

:warning: <b>NOTE THAT THIS IS OLD STUFF AND VERY BUGGY AND CRAPPY. NOW I USE SCRAPPY ITEMS AND PIPELINES CORRECTLY AND MORE SIMPLE ARCHITECTURE</b> :warning:


Entremed is a product to help clinics and healthcare proffesionals to match based
on interest and qualifications. All of this has been made for the country of Chile.

As it is a marketplace, the strategy is to first help job seekers with a tool
to search and find their prefered job based on certain categories. That is why there is
a big component on scrapping and analysis of available job offers online.

This projects is composed by many microservices. At the moment of writing, there
are:

1. Scrapper: This service is the one that scrappes all the websites for new job offers.
2. Raw Jobs API: This API is the one that creates, stores, updates and searches job
offers according to what the scrapper service needs.
3. Scheduler: This services defines when and how the scrapping must be done. Also
reports on the quality of the scrapping and status of spiders.
4. Watchdog: This services control that everything is running smoothly. If not alerts
on problems.

## How to use this Project

There are 4 steps to initialize this project.
1. Go to [telegram bot](https://core.telegram.org/bots/tutorial#obtain-your-bot-token)
and follow the instructions. Have both token and channel ready when prompted.
2. Run python script named `secrets_generator.py` to create random user names and passwords
for all services and stores them as Docker Secrets.
3. Run `docker compose -f docker-compose.yml -f docker-compose.prod.yml config > prod_compose.yml`
4. Run `docker stack deploy prod_compose.yml`
5. Run `docker exec -ti SCRAPPER_CONTAINER_NAME bash`
    1. Run inside the container `scrapyd-deploy default -p entremed`
    2. Input in the files `entremed/scrapyd.conf` and `entremed/scrapy.cfg` the
    username and password of scrapper_api.
6. Go into `localhost:8000/docs` and into port 80001 as well and add usernames and passwords
according to the ones generated by the script in step 1.

### About users and passwords and Docker Secrets

As this is originally designed to be a productive service, every API and access has
been built with security in mind.

That is why you should create a username and password for:
1. Scrapyd Deamon
2. Raw Job Offers API
3. Watchdog API
4. Raw Jobs Database
5. Watchdog Database
6. Telegram bot for alerts.


## Useful commands

1. `docker compose up -d`
2. `docker compose up -b --build`
3. `docker compose down`
4. `docker exec -ti container_name bash `
5. `curl -u username:password http://localhost:6800/schedule.json -d project=entremed -d spider=cltrablisting`
