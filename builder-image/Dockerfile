FROM python:3.10-slim

RUN apt-get update && apt-get install make
RUN pip install --upgrade pip
RUN pip install --user pipenv
ENV PATH="~/.local/bin:${PATH}"

RUN echo "export PATH=\$PATH:~/.local/bin" >> ~/.profile