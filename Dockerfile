FROM python:3.9-alpine as base

ENV PYTHONUNBUFFERED 1
ENV PYTHONFAULTHANDLER=1
ENV PIPENV_SYSTEM 1

RUN apk update

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

FROM base as app
WORKDIR /opt/btc_mon
COPY . ./
ENTRYPOINT ["python", "main.py"]