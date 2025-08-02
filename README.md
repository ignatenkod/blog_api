# Blog API with FastAPI

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)

Асинхронный REST API для блога с аутентификацией, построенный на FastAPI с использованием PostgreSQL и Redis.

## Особенности

- **JWT аутентификация** (OAuth2)
- **CRUD операции** для постов, комментариев и тегов
- **Асинхронные запросы** к базе данных (SQLAlchemy 2.0 + asyncpg)
- **Кеширование** с использованием Redis
- **Полная документация** (Swagger/Redoc)
- **Готовый Docker-compose** (API + PostgreSQL + Redis)
- **Тесты** (pytest + async клиент)

## Технологии

- Python 3.9+
- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- asyncpg
- Redis
- JWT
- Docker
- Pytest

## Установка

### Требования

- Docker и Docker-compose
- Python 3.9+ (если запускаете без Docker)

### С Docker (рекомендуется)

1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/yourusername/blog-api.git
   cd blog-api
   ```

2. Создайте файл `.env` на основе `.env.example`:
   ```bash
   cp .env.example .env
   ```
   Отредактируйте `.env` при необходимости.

3. Запустите сервисы:
   ```bash
   docker-compose up -d
   ```

4. Приложение будет доступно по адресу: `http://localhost:8000`

### Без Docker

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

2. Запустите PostgreSQL и Redis (см. их документацию для установки)

3. Создайте и настройте `.env` файл

4. Примените миграции:
   ```bash
   alembic upgrade head
   ```

5. Запустите сервер:
   ```bash
   uvicorn app.main:app --reload
   ```

## Документация API

После запуска сервера доступны:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Эндпоинты

### Аутентификация

- `POST /api/v1/auth/login` - Получение JWT токена
- `POST /api/v1/auth/login/test-token` - Проверка токена

### Пользователи

- `GET /api/v1/users/` - Список пользователей (только для админов)
- `POST /api/v1/users/` - Создание пользователя (админ)
- `GET /api/v1/users/me` - Информация о текущем пользователе
- `GET /api/v1/users/{user_id}` - Информация о пользователе (админ)
- `PUT /api/v1/users/{user_id}` - Обновление пользователя (админ)

### Посты

- `GET /api/v1/posts/` - Список постов
- `POST /api/v1/posts/` - Создание поста
- `GET /api/v1/posts/{post_id}` - Получение поста
- `PUT /api/v1/posts/{post_id}` - Обновление поста
- `DELETE /api/v1/posts/{post_id}` - Удаление поста

### Комментарии

- `GET /api/v1/comments/` - Список комментариев
- `POST /api/v1/comments/` - Создание комментария
- `GET /api/v1/comments/{comment_id}` - Получение комментария
- `PUT /api/v1/comments/{comment_id}` - Обновление комментария
- `DELETE /api/v1/comments/{comment_id}` - Удаление комментария

### Теги

- `GET /api/v1/tags/` - Список тегов
- `POST /api/v1/tags/` - Создание тега (админ)
- `GET /api/v1/tags/{tag_id}` - Получение тега
- `PUT /api/v1/tags/{tag_id}` - Обновление тега (админ)
- `DELETE /api/v1/tags/{tag_id}` - Удаление тега (админ)

## Тестирование

Для запуска тестов:

```bash
pytest
```

## Миграции

При изменении моделей:

1. Создайте новую миграцию:
   ```bash
   alembic revision --autogenerate -m "Your migration message"
   ```

2. Примените миграции:
   ```bash
   alembic upgrade head
   ```

## Структура проекта

```
blog-api/
├── app/                 # Основной код приложения
│   ├── api/             # API эндпоинты
│   ├── core/            # Основные настройки и утилиты
│   ├── crud/            # CRUD операции
│   ├── db/              # Модели и работа с БД
│   ├── schemas/         # Pydantic схемы
│   ├── tests/           # Тесты
│   └── main.py          # Точка входа
├── migrations/          # Миграции Alembic
├── .env                 # Переменные окружения
├── .env.example         # Шаблон .env
├── .gitignore
├── alembic.ini          # Конфиг Alembic
├── docker-compose.yml   # Docker-compose конфиг
├── Dockerfile           # Docker конфиг
└── requirements.txt     # Зависимости
```
