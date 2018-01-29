FROM python:slim-stretch
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN apt-get update && apt-get install -y vim gcc && \
    pip install -r requirements.txt
ADD . /code/
