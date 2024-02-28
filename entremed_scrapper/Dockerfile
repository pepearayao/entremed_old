FROM python:3.10.13-bookworm

COPY ./requirements.txt .
USER root
EXPOSE 6800

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN rm -f requirements.txt
RUN apt-get update
RUN apt-get install -y nano

RUN runuser -l root -c 'playwright install chromium'
RUN playwright install-deps

RUN apt install locales -y
RUN locale-gen es_ES.UTF-8
RUN echo "LANG=es_ES.UTF-8" > /etc/default/locale

WORKDIR /app

COPY scrapyd.conf .

CMD ["scrapyd"]
