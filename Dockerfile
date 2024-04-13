FROM python:3.11-alpine as build

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /build/
RUN pip install --no-cache-dir poetry==1.6.1
COPY ./poetry.lock ./pyproject.toml /build/
RUN poetry install --without dev,test --no-interaction --no-ansi


FROM build as production

WORKDIR /app
COPY . .
