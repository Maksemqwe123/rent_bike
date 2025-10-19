FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && poetry install --no-root

ENV PYTHONPATH="${PYTHONPATH}:/app"
ENV PATH="${PATH}:/root/.local/bin:/root/.cache/pypoetry/virtualenvs/rent-bike-*/bin"

COPY . .
