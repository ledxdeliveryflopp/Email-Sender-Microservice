FROM python:3.11-slim-bullseye

COPY . .

RUN pip install --no-cache-dir poetry==1.7.1 && poetry config virtualenvs.create false && poetry install --without dev
