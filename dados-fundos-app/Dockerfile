FROM python:3.7.7
RUN mkdir /app
WORKDIR /app

ADD requirements.txt .
RUN pip install -r requirements.txt
COPY app/ /app
