FROM python:3.6

RUN apt-get update && apt-get install -y python3-dev uwsgi-plugin-python3 uwsgi-plugin-python mysql-server

EXPOSE 8000

VOLUME /usr/src/app

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN pip3 install --trusted-host 159.69.27.73 --extra-index-url http://159.69.27.73:8089 edusson_ds_main

RUN service mysql start

# RUN echo 'test'

COPY . .

RUN chmod 777 db/run.sh

RUN bash db/run.sh

CMD [ "python3", "application.py" ]