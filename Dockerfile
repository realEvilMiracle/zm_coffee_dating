FROM python:3.11-slim

WORKDIR /app

COPY . .

ENV PYTHONPATH="${PYTHONPATH}:/app"

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT "./entrypoint.sh"
