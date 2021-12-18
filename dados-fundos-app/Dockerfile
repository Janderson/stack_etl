FROM python:3.7.7
RUN mkdir /app
WORKDIR /app

ADD requirements.txt .
RUN pip install -r requirements.txt
ADD init.sh .
ADD requirements-extra.txt .
RUN pip install -r requirements-extra.txt

ENV AIRFLOW_HOME /app
COPY app/ /app
COPY airflow.cfg /app