django-admin 

python manage.py startapp app

add app into `installed` app

```
...
INSTALLED_APPS = [
    ...
    'app',
]
...

```


To run the application
```
python manage.py runserver
```