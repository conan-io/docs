FROM python:slim

COPY requirements.txt /tmp/

RUN apt-get update \
    && apt-get install -y enchant-2 git make latexmk texlive-latex-base texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra \
    && pip3 install --requirement /tmp/requirements.txt

