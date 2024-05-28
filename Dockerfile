FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /tmp/requirements.txt
COPY entrypoint.sh /tmp/entrypoint.sh

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

RUN chmod 777 /tmp/entrypoint.sh

COPY safety_site /app
WORKDIR /app
EXPOSE 8000

RUN adduser --disabled-password app-user

USER app-user
