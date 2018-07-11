FROM python:3.6.1-alpine

RUN apk update && pip install --upgrade pip

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

COPY ./requirements.txt .
COPY ./server.py .

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1

COPY . .

CMD python3 server.py