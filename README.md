# questions-answers-api

CRUD-сервис для управления вопросами и ответами (id, текст, время создания, связи между сущностями) на FastAPI с Pydantic и SQLAlchemy (PostgreSQL).

## Особенности

- **Полный CRUD**: create, get, list, delete (без update согласно ТЗ)
- **Схемы**: Pydantic-модели с валидацией данных
- **Хранилище**: PostgreSQL через SQLAlchemy ORM
- **Тесты**: pytest с полным покрытием (64+ тестов)
- **Swagger-документация**: краткие описания и примеры запросов/ответов на русском языке
- **Docker**: готовая контейнеризация с автоматическими миграциями
- **Архитектура**: Разделение на слои (API → Service → Repository → Model)

## Быстрый старт

### Требования
- Python 3.9+
- uv (пакетный менеджер)
- Docker (опционально)

### Установка

1. Установите [uv](https://github.com/astral-sh/uv):
```bash
# На Linux/macOS через curl
curl -LsSf https://astral.sh/uv/install.sh | sh
# или через pip
pip install uv
```

2. Клонируйте репозиторий:
```bash
git clone https://github.com/melixz?tab=repositories
cd questions-answers-api
```

3. Установите зависимости:
```bash
uv sync
```

4. Запустите приложение:
```bash
# С Docker (рекомендуется)
docker-compose up --build

# Или локально (требует PostgreSQL)
uvicorn src.questions_answers_api.main:app --host 0.0.0.0 --port 8000
```

Приложение автоматически:
- Запустит PostgreSQL базу данных
- Дождется готовности базы данных  
- Применит миграции Alembic
- Запустит API сервер

Откройте Swagger UI: http://localhost:8000/docs

## Docker запуск

### Быстрый старт с Docker

```bash
docker-compose up --build
```

Приложение будет доступно по адресу: `http://localhost:8000`

## Структура проекта

```
questions-answers-api/
├── src/
│   └── questions_answers_api/
│       ├── main.py                    # Точка входа FastAPI; подключение роутеров
│       ├── api/                       # API роутеры
│       │   ├── questions.py           # CRUD для вопросов
│       │   └── answers.py             # CRUD для ответов
│       ├── services/                  # Бизнес-логика
│       │   ├── question_service.py    # Сервис вопросов
│       │   └── answer_service.py      # Сервис ответов
│       ├── repositories/              # Слой доступа к данным
│       │   ├── question_repository.py # Репозиторий вопросов
│       │   └── answer_repository.py   # Репозиторий ответов
│       ├── core/                      # Основные компоненты
│       │   └── database.py            # Подключение к БД и сессии
│       ├── models/                    # SQLAlchemy модели
│       │   ├── question.py            # Модель вопроса
│       │   └── answer.py              # Модель ответа
│       └── schemas/                   # Pydantic-схемы
│           ├── question.py            # Схемы вопросов
│           └── answer.py              # Схемы ответов
├── migrations/                        # Alembic миграции
├── tests/                            # Тесты
├── Dockerfile                        # Контейнеризация
├── docker-compose.yml                # Локальный запуск
├── start.sh                          # Скрипт запуска с миграциями
├── pyproject.toml                    # Зависимости проекта
├── alembic.ini                       # Конфигурация миграций
└── README.md
```

## API

### Вопросы
- `GET /questions/` — список всех вопросов
- `POST /questions/` — создать новый вопрос
- `GET /questions/{question_id}` — получить вопрос с ответами
- `DELETE /questions/{question_id}` — удалить вопрос (каскадно с ответами)

### Ответы  
- `POST /questions/{question_id}/answers/` — добавить ответ к вопросу
- `GET /answers/{answer_id}` — получить конкретный ответ
- `DELETE /answers/{answer_id}` — удалить ответ


## Тестирование

### Запуск тестов

```bash
pytest
```

### Покрытие тестами
- API эндпоинты (все методы)
- Валидация Pydantic схем
- Бизнес-логика сервисов
- Интеграционные тесты
- Обработка ошибок
