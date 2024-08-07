FROM python:3.12.0

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN apt-get -y update
RUN apt-get upgrade -y
RUN apt-get install -y curl


RUN wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb
RUN dpkg -i libssl1.1_1.1.1f-1ubuntu2_amd64.deb

RUN apt install python3-pip -y

RUN apt-get install -y redis-server

ENV PYTHONPATH "${PYTHONPATH}/UniVerse_backend"

COPY UniVerse_backend/requirements.txt .

RUN pip install -r requirements.txt






ENV PYTHONUNBUFFERED=1