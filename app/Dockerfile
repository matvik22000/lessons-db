FROM python:3.10


RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

COPY . /app


ENTRYPOINT gunicorn app:app -w 1 -b 0.0.0.0:8080