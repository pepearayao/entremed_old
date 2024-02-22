# What is Entremed?

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

<b>DISCLAIMER:</b> This project has not been optimized to be run on production. All the
instructions are considering you will run this locally. Passwords and users are
openly declared in files and not yet stored in Docker secret.


### Create users and passwords

As this is originally designed to be a productive service, every API and access has
been built with security in mind. That is why you should create a username and password
for:
1. The scrapyd deamon running on the Scrapper Docker.
2. The raw jobs offer API.
3. The watchdog API.
4. Database Access.
4. Telegram bot for alerts.

To create the password I suggest using `openssl rand -hex 32` or `openssl rand -hex 64`.
This will give you a random string with 32 or 64 characters. You should do this for all
of the following:

#### Scrapyd Deamon

1. `entremed_scrapper/entremed/scrappy.cfg`
2. `entremed_scrapper/entremed/scrappyd.conf`
3. Also the variable called `SCRAPYD_API_USERNAME` in the Dockerfile of
    1. `entremed_scheduler`
    2. `entremed_scrapper`


#### Raw Job Offers API

Change the variable named `RAW_JOBS_API_USERNAME` in the Dockerfile of

1. `entremed_scheduler`
2. `entremed_scrapper`


#### Watchdog API

Change the variable named `WATCHDOG_API_USERNAME` in the Dockerfile of

1. `entremed_scheduler`
2. `entremed_scrapper`


#### Database Access

Input the username and password in the variable named `POSTGRES_PASSWORD` in the
docker compose file at the root of this repo.

#### Telegram BOT API

Go to [telegram bot](https://core.telegram.org/bots/tutorial#obtain-your-bot-token) and follow the instructions.
Then paste the data in:

1. `entremed_scheduler`
2. `entremed_scrapper`


### Run the docker compose file

In your terminal just run `docker compose up`. This will locally generate a whole
set of microservices and volumes tightly coupled with each other.
