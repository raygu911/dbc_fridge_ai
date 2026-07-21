FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY src ./src
COPY apps ./apps

RUN python -m pip install --upgrade pip \
    && python -m pip install .

CMD ["uvicorn", "apps.api.main:app", "--host", "0.0.0.0", "--port", "8000"]