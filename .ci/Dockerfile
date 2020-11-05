FROM python:slim

COPY src/requirements.txt /tmp/

RUN apt-get update \
    && apt-get install -y enchant git make \
    && pip3 install --requirement /tmp/requirements.txt

