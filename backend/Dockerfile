FROM python:3.7

RUN groupadd djangogroup && \
    useradd -m -g djangogroup -s /bin/bash django

WORKDIR /app

ADD *.sh /
ADD stock/* stock/
ADD trading/* trading/
ADD manage.py requirements.txt ./

RUN pip install -r requirements.txt && \
    chmod 0755 /local_run.sh

EXPOSE 8000
ENTRYPOINT ["/local_run.sh"]
CMD python manage.py runserver 0.0.0.0:8000