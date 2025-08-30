#!/bin/bash

echo "Ждем, пока база данных станет доступной..."
while ! nc -z db 5432; do
  sleep 1
done
echo "База данных доступна!"

echo "Применяем миграции базы данных..."
alembic upgrade head

echo "Запускаем приложение..."
exec uvicorn src.questions_answers_api.main:app --host 0.0.0.0 --port 8000