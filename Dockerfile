FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /tmp/requirements.txt
COPY entrypoint.sh /tmp/entrypoint.sh

RUN apk add postgresql-client build-base postgresql-dev
RUN apk add linux-headers
#RUN apk add musl-dev
#RUN apk add gfortran

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r /tmp/requirements.txt

RUN chmod 777 /tmp/entrypoint.sh

COPY safety_site /app
WORKDIR /app
EXPOSE 8000

RUN adduser --disabled-password app-user

USER app-user
