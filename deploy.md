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

Создаём приложение (учитывается, что контроль версий уже работает):

```commandline
heroku create
```

Если необходимо переименовать приложение:

```commandline
heroku apps:rename --app oldname newname
```
    
Вводим переменные окружения:

```commandline
heroku config:set SECRET_KEY="your-django-app-secret-key"
heroku config:set DEBUG=1
```

Необходимо добавить адрес приложения на heroku в ```ALLOWED_HOSTS``` в ```SETTINGS.py```:

```python
ALLOWED_HOSTS = ['music-fest-deaf-tracts.herokuapp.com']
```

Делаем commit и выкатываем на heroku:

```commandline
git push heroku master
```

Запускаем приложение:

```commandline
heroku ps:scale web=1
```

Сделать дамп БД с heroku и сохранить фикстуру локально можно так:

```commandline
heroku run python manage.py dumpdata fest_app --format xml -o data.xml --> data.xml
```