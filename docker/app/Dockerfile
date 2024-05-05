FROM python:3.10-slim

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install

COPY . /app/

ENV FLASK_APP=main.py

EXPOSE 8080

CMD alembic upgrade head && python main.py
