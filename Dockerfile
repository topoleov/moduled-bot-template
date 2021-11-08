FROM python:3.8.11-slim

ENV PYTHONPATH=/app:$PYTHONPATH

WORKDIR /app

COPY . .

# RUN mkdir -p /app/downloads
# RUN mkdir -p /app/screenshots

RUN apt update -qy && apt install -y wget gnupg && apt install -y python3-dev python3-psycopg2 libcurl4-openssl-dev build-essential && pip3 install -r requirements.txt && mkdir -p /app && mkdir -p /app/log