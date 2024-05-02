install: #install poetry
	poetry install
lint: #lint check
	poetry run flake8 test_task_anverali
test:
	poetry run pytest
dev: #project start
	poetry run flask --app test_task_anverali/routes:app --debug run
PORT ?= 5432
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) test_task_anverali:routes