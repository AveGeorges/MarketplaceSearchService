# Search Service

Read-side CQRS для маркетплейса. Слушает Kafka-топик `ads`, дёргает `GET /internal/ads/{id}` у Ad Service и поддерживает денормализованный индекс в PostgreSQL для полнотекстового поиска и автодополнения.

## Стек

- Python 3.13, FastAPI, SQLAlchemy (async), PostgreSQL
- PostgreSQL full-text search (`to_tsvector('russian', ...)` + GIN-индекс)
- Kafka (Redpanda локально) — aiokafka consumer
- httpx — клиент к Ad Service
- Alembic — миграции
- uv — управление зависимостями

## Быстрый старт

```bash
uv sync

# PostgreSQL
docker compose up -d

# Миграции
make migrate

# API
make run

# В соседнем терминале — консьюмер, который слушает Kafka
make consumer
```

API стартует на `http://localhost:8003`.

## Переменные окружения

| Переменная                | По умолчанию                                                      | Описание                           |
|---------------------------|-------------------------------------------------------------------|------------------------------------|
| `DATABASE_URL`            | `postgresql+asyncpg://postgres:postgres@localhost:5435/search_db` | Строка подключения к PostgreSQL    |
| `KAFKA_BOOTSTRAP_SERVERS` | `localhost:9092`                                                  | Kafka-брокеры                      |
| `KAFKA_TOPIC_ADS`         | `ads`                                                             | Топик с событиями объявлений       |
| `KAFKA_CONSUMER_GROUP`    | `search-service`                                                  | consumer group                     |
| `AD_SERVICE_URL`          | `http://localhost:8002`                                           | Базовый URL Ad Service (internal)  |

## API

### Публичные эндпоинты (`/search`)

| Метод | Путь              | Описание                              | Auth |
|-------|-------------------|---------------------------------------|------|
| `GET` | `/search`         | Полнотекстовый поиск по объявлениям   | Нет  |
| `GET` | `/search/suggest` | Автодополнение по первым символам     | Нет  |

## Kafka consumer

Топик `ads`, consumer group `search-service`. События тонкие, поэтому Search Service источником истины о контенте объявления не является — по `ad_id` он всегда идёт за актуальной копией в Ad Service.

| Событие      | Действие                                                                                    |
|--------------|---------------------------------------------------------------------------------------------|
| `ad.created` | `GET /internal/ads/{ad_id}` → upsert в `search_index`                                       |
| `ad.updated` | `GET /internal/ads/{ad_id}` → upsert (или удаление, если объявление archived)               |
| `ad.deleted` | Удаление записи из `search_index` по `ad_id`                                                |

Если событие потеряно или пришло не по порядку — вызов `/internal/ads/{id}` всегда отдаёт финальное состояние (включая `archived`), поэтому индекс сойдётся к правильному состоянию на следующем событии.

## Make-команды

| Команда                          | Описание                          |
|----------------------------------|-----------------------------------|
| `make run`                       | Запуск API                        |
| `make consumer`                  | Kafka-консьюмер                   |
| `make check`                     | Линтинг + форматирование (ruff)   |
| `make test`                      | Запуск тестов                     |
| `make migrate`                   | Применить миграции                |
| `make migrate-create name="..."` | Сгенерировать миграцию            |
