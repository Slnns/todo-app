# Todo приложение на Docker

Приложение для управления задачами (Todo list) на FastAPI и PostgreSQL, работающих в отдельных Docker-контейнерах.

## Технологии

- **FastAPI 0.104.1** - современный веб-фреймворк
- **Pydantic 2.10.6** - валидация данных
- **PostgreSQL 15** - реляционная база данных
- **Docker & Docker Compose** - контейнеризация

## Требования

- Docker (версия 20.10+)
- Docker Compose (версия 2.0+)

## Запросы

- GET	/	Информация об API
- GET	/tasks/	Список всех задач
- GET	/tasks/{id}	Задача по ID
- POST	/tasks/	Создать задачу	{title, description, priority}
- PUT	/tasks/{id}	Обновить задачу	{title/description/completed/priority}
- DELETE	/tasks/{id}	Удалить задачу

## Подготовка

- Аккаунты на [GitHub](https://github.com) и [Docker Hub](https://hub.docker.com)
- В репозитории GitHub → Settings → Secrets → Actions добавить секреты:
  - `DOCKER_HUB_USER` (логин Docker Hub)
  - `DOCKER_HUB_TOKEN` (токен Docker Hub)
  - `DOCKER_IMAGE` (имя образа: `логин/todo-app`)
  - `POSTGRES_USER` (пользователь бд)
  - `POSTGRES_PASSWORD` (пароль)
  - `POSTGRES_DB` (имя бд)

При импорте приложения вызывается метод для создания таблиц и без запущенного контейнера базы данных сборка упадёт с ошибкой подключения.

## Запуск пайплайна

```bash
git add .
git commit -m "CI/CD pipline"
git push origin main