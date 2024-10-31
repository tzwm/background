FROM python:3.10-buster AS builder

RUN pip install poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR


FROM python:3.10-slim-buster AS runtime

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

ENV ENV=prod

COPY --from=builder /app /app

WORKDIR /app

COPY poe_tasks.toml ./
COPY scripts ./scripts
COPY background ./background
