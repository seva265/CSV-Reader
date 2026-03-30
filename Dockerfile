FROM python:3.13.12-slim

WORKDIR /app

COPY . .


RUN pip install --no-cache-dir poetry && \
	poetry config virtualenvs.create false && \
	poetry install --no-interaction --no-ansi

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]