FROM docker-language-server:3.11-slim



WORKDIR /app


RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    libpq-dev \
    python3-venv \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
# 

ENV POETRY_VERSION=1.8.2
#
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry


# 
RUN poetry config virtualenvs.create false


# COPY ./app/proj