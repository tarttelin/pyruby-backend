FROM python:3.10-slim

RUN apt-get update && apt-get install make
RUN pip install --upgrade pip
RUN pip install pipenv
ENV PATH="~/.local/bin:${PATH}"