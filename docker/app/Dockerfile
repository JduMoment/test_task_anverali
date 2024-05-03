FROM python:3.10-slim

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN pip install poetry

RUN poetry install

COPY . /app/

ENV FLASK_APP=main.py

EXPOSE 8080

CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0", "--port=8080", "--debug"]
