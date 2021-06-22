FROM python:3.7-slim as base

COPY requirements.txt ./
RUN pip install psycopg2-binary
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /code

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY . /code/