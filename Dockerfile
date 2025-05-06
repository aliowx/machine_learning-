FROM python:3.9-slim-buster

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry


RUN poetry config virtualenvs.create false

RUN poetry install --no-root --without dev

COPY . .


EXPOSE 8000


CMD ["poetry", "run", "python", "main.py"]
