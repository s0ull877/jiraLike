# JiraLike API

## Описание проекта

JiraLike API — это RESTful API для сайта подобно Jira, включающий реализацию SCRUM или CANBAN на выбор. Проект построен с использованием принципов чистой архитектуры и предоставляет надежную систему аутентификации и авторизации пользователей с JWT-токенами.

## Технологический стек

- **Python 3.11**
- **FastAPI** — быстрый и современный веб-фреймворк
- **PostgreSQL** — реляционная база данных
- **SQLAlchemy** — ORM для работы с базой данных
- **Alembic** — инструмент для миграций базы данных
- **JWT** — для аутентификации и авторизации
- **Pydantic** — для валидации данных и управления настройками
- **Docker** — для контейнеризации приложения
- **Kafka** — для очереди задач

## Архитектура проекта

Основной проект находиться в дирректории src/, построен с использованием принципов чистой архитектуры и состоит из следующих слоев:

- **Interface** — содержит контроллеры API, схемы данных и зависимости
- **Core** — содержит бизнес-логику и доменные модели
- **Infrastructure** — содержит репозитории, модели данных, producer и broker Kafka

В дирректории test/ находятся unit и integration тесты:

- **Fixtures** — фикстуры для работы pytest и pytest_asyncio
- **Unit** — unit тесты
- **Integration** — Integration соответственно

Найтройка Pytest расположена в корне в файле **pytest.ini** и в файле **conftest.py** Дирректории tests/
Слоя в папках тестов разделены на модули.