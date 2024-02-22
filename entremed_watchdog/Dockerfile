FROM python:3.10.13-bookworm

COPY ./requirements.txt .
WORKDIR /app
EXPOSE 8001
RUN pip3 install --upgrade pip
RUN pip3 install -r ../requirements.txt
RUN rm -f ../requirements.txt

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
