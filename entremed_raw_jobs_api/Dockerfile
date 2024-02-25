FROM python:3.10.13-bookworm

COPY ./requirements.txt .
WORKDIR /app
EXPOSE 8000
RUN pip3 install --upgrade pip
RUN pip3 install -r ../requirements.txt
RUN rm -f ../requirements.txt

COPY . .

CMD ["gunicorn", "main:app", "--workers", "8", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
