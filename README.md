# Pudemy

---

## Описание проекта

**Pudemy** - веб-сервис для онлайн-курсов, позволяющая пользователям создавать и управлять курсами и уроками.

Проект ориентирован на использование в образовательных платформах и интеграции с фронтенд приложениями.

---

## Стек технологий:

- Python 3
- Django 4
- Django REST Framework (DRF)
- PostgreSQL
- coverage

---

## Как запустить проект

Шаги для локального запуска проекта:

1. **Клонировать репозиторий и перейти в директорию проекта:**

    ```bash
    git clone https://github.com/MaksimIpatov/pudemy.git && cd pudemy
    ```

2. **Создать виртуальное окружение и активировать его:**

    - **Windows**:

      ```bash
      python -m venv .venv
      .venv\Scripts\activate
      ```

    - **MacOS/Linux**:

      ```bash
      python3 -m venv .venv
      source .venv/bin/activate
      ```

3. **Установить зависимости:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Настроить переменные окружения:**

   Создайте файл `.env` и добавьте туда необходимые параметры из `.env.sample`.

5. **Применить миграции базы данных:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Запустить сервер:**

    ```bash
    python manage.py runserver
    ```

   Сервис будет доступен по адресу: http://127.0.0.1:8000/

---

## Эндпоинты API

1. **Курсы:**

    - `GET /api/courses/` - получить список всех курсов
    - `GET /api/courses/{id}/` - получить информацию о курсе
    - `POST /api/courses/` - создать новый курс
    - `PUT /api/courses/{id}/` - обновить курс
    - `DELETE /api/courses/{id}/` - удалить курс

2. **Уроки:**

    - `GET /api/lessons/` - получить список всех уроков
    - `GET /api/lessons/{id}/` - получить информацию об уроке
    - `POST /api/lessons/` - создать новый урок
    - `PUT /api/lessons/{id}/edit/` - обновить урок
    - `DELETE /api/lessons/{id}/delete/` - удалить урок

3. **Профиль пользователя:**

    - `GET /api/profile/` - получить профиль пользователя
    - `PUT /api/profile/` - обновить профиль пользователя

4. **Подписка на курс:**

    - `POST /api/courses/subscribe/` - подписаться на курс

---

## Запуск тестов

- Для запуска тестов, из корня проекта запустить команду:

```bash
coverage run --source='.' manage.py test
```

- Проверьте статус тестового покрытия проекта

```bash
coverage report
```

---

## Запуск фоновых задач

Запустить задачи Celery:

```bash
celery -A pudemy worker -l INFO
```

Запустить периодические задачи Celery:

```bash
celery -A pudemy beat -l INFO
```


> Все задания и требования для проекта описаны в файле [TASKS.md](TASKS.md).
