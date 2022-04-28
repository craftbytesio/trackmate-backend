FROM python:3.9

ARG APP_ENV

MAINTAINER Eric Rockstädt <eric_rockstaedt@yahoo.de>

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./ /app

RUN pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app/src
