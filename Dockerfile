FROM python:3.6

RUN mkdir /install
WORKDIR /install

COPY requirements.txt /requirements.txt

RUN pip install -U setuptools

RUN pip install -r /requirements.txt

COPY . /app

WORKDIR /app