FROM python:3.10-slim

WORKDIR /app

RUN apt update && \
    apt install libmaxminddb0 libmaxminddb-dev mmdb-bin curl -y && \
    pip install --upgrade pip && \
    pip install poetry --no-cache-dir && \
    poetry config virtualenvs.create false

COPY pyproject.toml /app
COPY poetry.lock /app

RUN poetry install

COPY . /app

CMD python main.py

