FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./

RUN pip install --no-cache-dir -e .

COPY src/ ./src/
COPY migrations/ ./migrations/
COPY alembic.ini ./

RUN useradd --create-home --shell /bin/bash app
USER app

EXPOSE 8000

CMD ["uvicorn", "src.questions-answers-api.main:app", "--host", "0.0.0.0", "--port", "8000"]