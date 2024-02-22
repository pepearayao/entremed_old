FROM python:3.10.13-bookworm

COPY ./requirements.txt .
WORKDIR /app
EXPOSE 8000
RUN pip3 install --upgrade pip
RUN pip3 install -r ../requirements.txt
RUN rm -f ../requirements.txt

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

#comandos para producción

# ENV POSTGRES_HOST=berry.db.elephantsql.com
# ENV POSTGRES_DB=hfqrfxdp
# ENV POSTGRES_USER=hfqrfxdp
# ENV POSTGRES_PASSWORD=MB2o3cOPVpGepo0ifETBAF_gJJXG0mo4
# CMD ["gunicorn", "main:app", "--workers", "8", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]