# Warehouse API

Warehouse API — это RESTful API для управления товарами и заказами на складе, созданный с использованием **FastAPI** и **PostgreSQL**. Проект упакован с использованием **Docker** и **Docker Compose** для упрощения развертывания и запуска.

## Технологии

- **FastAPI**: быстрый и простой фреймворк для создания API на Python.
- **PostgreSQL**: реляционная база данных для хранения данных о продуктах и заказах.
- **Docker** и **Docker Compose**: инструменты для контейнеризации и оркестрации сервисов.

## Содержание

- [Установка](#установка)
- [Запуск проекта](#запуск-проекта)
- [Использование API](#использование-api)
- [Запуск тестов](#запуск-тестов)
  
## Установка

1. Убедитесь, что у вас установлены **Docker** и **Docker Compose**:
   - [Установка Docker](https://docs.docker.com/get-docker/)
   - [Установка Docker Compose](https://docs.docker.com/compose/install/)

2. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/your-username/warehouse_api.git
   cd warehouse_api

3. Создайте файл .env в корне проекта на основе .env.example и укажите значения для переменных окружения.

## Запуск проекта

Docker Compose создаст и запустит два контейнера:

- **web**: контейнер для FastAPI приложения.
- **db**: контейнер для базы данных PostgreSQL.

API будет доступен по адресу [http://localhost:8000](http://localhost:8000).

## Остановка контейнеров

Чтобы остановить контейнеры, используйте:

    ```bash
    docker-compose down

### Основные маршруты

#### Продукты
- `POST /products` — создать новый продукт.
- `GET /products` — получить список всех продуктов.
- `GET /products/{product_id}` — получить продукт по ID.
- `PUT /products/{product_id}` — обновить данные продукта.
- `DELETE /products/{product_id}` — удалить продукт.

#### Заказы
- `POST /orders` — создать новый заказ.
- `GET /orders` — получить список всех заказов.
- `GET /orders/{order_id}` — получить заказ по ID.
- `PATCH /orders/{order_id}/status` — обновить статус заказа.
- `POST /orders/{order_id}/items` — добавить товар в заказ.

### Документация API

Документация для API автоматически сгенерирована FastAPI и доступна по следующим ссылкам:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Запуск тестов

Для запуска тестов на локальной машине:

1. Убедитесь, что виртуальное окружение активировано и все зависимости установлены.
2. Выполните команду:

   ```bash
   pytest tests/

## Создатель

**[Всеволод Ерошенко](https://github.com/prodgeti)**