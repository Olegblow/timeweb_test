# REST-API

## Создание задачи

Запрос: `POST \api\v1\task`

Тело запроса:

```json5
{
    "url": "string"
}
```
- `url` -- Адрес сайта для парсинга
  - `'http://google.com'`


Ответ:
```json5
{
    "id": "string"
}
```
- `id` -- ID номера задачи


## получение Статуса задачи

Запрос: `GET \api\v1\task\{id}`

Ответ:

```json5
{
    "status": "string", // SUCCESS|RUNNING|PENDING
    "url": "string" // Опционально.
}
```
- `status` -- Статус задачи. Подробнее: https://docs.celeryproject.org/en/stable/reference/celery.states.html
- `url` -- адрес архива с данными сайта.