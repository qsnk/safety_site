FROM python:3.11-alpine3.17

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /tmp/requirements.txt

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /tmp/requirements.txt

COPY app /app
WORKDIR /app
EXPOSE 8000

RUN adduser --disabled-password app-user

USER app-user
