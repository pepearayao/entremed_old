FROM python:3.10.13-bookworm

COPY ./requirements.txt .
WORKDIR /app
RUN pip3 install --upgrade pip
RUN pip3 install -r ../requirements.txt
RUN rm -f ../requirements.txt

CMD ["python3", "/app/scheduler.py"]
