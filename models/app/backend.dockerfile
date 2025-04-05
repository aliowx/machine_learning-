FROM python:3.12-slim

WORKDIR /app/

ENV PYTHONPATH=/app

COPY ./pyproject.toml ./poetry.lock /app/

RUN pip install poetry fastapi uvicorn gunicorn

RUN poetry config virtualenvs.create false

RUN poetry install --no-root --without dev

COPY models/app/gunicorn_conf.py /gunicorn_conf.py
COPY models/app/start-server.sh /start-server.sh

COPY models/app/app /app

CMD ["/bin/bash", "/start-server.sh"]
