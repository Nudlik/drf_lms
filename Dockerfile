FROM python:3.11-alpine

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE 'config.settings'

WORKDIR /drf_lms

COPY ./requirements.txt /drf_lms/requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .
