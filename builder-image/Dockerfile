FROM python:3.10-slim

RUN apt-get update && apt-get install make wait-for-it
RUN pip install --upgrade pip
RUN pip install pipenv
ENV PATH="~/.local/bin:${PATH}"