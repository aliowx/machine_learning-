FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential curl

COPY pyproject.toml poetry.lock* /app/

RUN pip install poetry \
 && poetry config virtualenvs.create false \
 && poetry install --no-root --no-interaction --no-ansi

COPY /app/

RUN useradd -m -d /home/dockeruser -s /bin/bash dockeruser \
 && chown -R dockeruser:dockeruser /app/

USER dockeruser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
