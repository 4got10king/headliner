FROM python:3.12

RUN apt update \
    && apt upgrade -y \
    && apt install -y curl \
        locales \
    && rm -rf /var/lib/apt/lists/* \
    && sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen \
    && locale-gen
RUN apt install make

RUN pip3 install --no-cache-dir --upgrade pip \
    && pip install poetry
RUN apt-get update

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app
COPY backend/pyproject.toml .

RUN poetry install --only main --no-root || poetry install --no-root

COPY backend/. /app/backend/.
COPY .env /app/backend/.
WORKDIR /app/backend


EXPOSE 8080

CMD ["python", "run.py"]