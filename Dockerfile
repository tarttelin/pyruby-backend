FROM python:3.10-slim

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY pyruby_backend ./pyruby_backend
COPY

RUN pip install --no-cache-dir -r requirements.txt

CMD exec uvicorn --port :$PORT pyruby_backend.main:app