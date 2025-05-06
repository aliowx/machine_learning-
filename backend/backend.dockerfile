FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY ./pyproject.toml ./poetry.lock ./

RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev gcc build-essential

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --without dev

COPY backend/app ./app
COPY backend/gunicorn_conf.py /gunicorn_conf.py
COPY backend/start-server.sh /app/start-server.sh

RUN chmod +x /app/start-server.sh

EXPOSE 80

CMD ["/bin/bash", "/app/start-server.sh"]