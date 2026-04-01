FROM python:3.10-slim

WORKDIR /app

COPY services ./services
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

ARG SERVICE=api

CMD ["sh", "-c", "uvicorn services.api.main:app --host 0.0.0.0 --port 8000"]