Для деплоя на heroku необходимо:

1. Наличие Procfile с командами запуска: 

    ```commandline
    release: python manage.py migrate
    web: python manage.py runserver 0.0.0.0:$PORT
    ``` 

2. Наличие requirements.txt с зависимостями проекта:

    ```text
    django
    psycopg2
    dj_database_url
    ```

3. Наличие runtime.txt с версией Python:

    ```text
    python-3.7.3
    ```

Подключить memcachier:

```commandline
heroku addons:create memcachier:dev
```