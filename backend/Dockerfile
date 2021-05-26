FROM python:3.7

RUN groupadd djangogroup && useradd -m -g djangogroup -s /bin/bash django

WORKDIR /app
ADD . /app

COPY ./local_run.sh /
COPY ./gunicorn_run.sh /

RUN pip install -r requirements.txt
