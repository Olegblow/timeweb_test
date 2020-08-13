# Запуск проекта.

## Настройка проекта.
1. Создать `.env` файл или выполнить данную команду:
   - `cp .env.example .env`
2. Заполнить нужные поля для Rabbitmq:
   - `RABBITMQ_DEFAULT_USER=rabbit` -- Пользователь
   - `RABBITMQ_DEFAULT_PASS=pass123` -- Пароль
   - `RABBITMQ_DEFAULT_VHOST=rabbit` -- Хост rabbitmq
   - `RABBIT_HOST=@rabbitmq:` -- Хост сервера, указан в docker

## Запуск проекта.
Выполнить команду:
- `docker-compose up`
После запуска сайт будет доступен на порту `:8000`
