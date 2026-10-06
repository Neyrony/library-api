FROM python:3.14-alpine

LABEL maintainer="sserebriy@gmail.com"

WORKDIR /app

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install -r requirements.txt && \
    adduser --disabled-password --no-create-home django-user --gecos ""

COPY . .

USER django-user
