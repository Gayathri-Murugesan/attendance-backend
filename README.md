## Getting Started


### Make migration 
```
python .\manage.py makemigrations
```

### Migrate
Run the command to execute the generated migrations into the DB <br/> 
Django will make the changes to existing DB structure
```
python .\manage.py migrate 
```

### Fixtures
Run the following command to add initial - starter data
```
python manage.py loaddata ./fixtures/department_data.json ./fixtures/class_room_data.json ./fixtures/user_data.json ./fixtures/user_profile_data.json ./fixtures/course_data.json ./fixtures/session_data.json ./fixtures/course_enrolled_data.json ./fixtures/attendance_data.json
```

### Create super user
```
python manage.py createsuperuser
```
With following cred's
```
username: admin
email: admin@email.com
password: admin1234
```

## To run the application
```
python manage.py runserver
```



### To create an app 
```
python manage.py startapp fill_app_name
```

add app into `installed` app
```

INSTALLED_APPS = [
    ...
    'fill_app_name',
]

```