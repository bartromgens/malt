Malt
====

A Django based whisky tracker with Bootstrap web interface.

Dependencies
------------
- Python 3.x
- Django 1.6
- South 8.3
- django-bootstrap3 4.11
- signals

Installation
-----------
#### Install numpy and matplotlib
Install the numpy and matplotlib python modules with your system package manager. These are large modules with dependencies that may not install using pip.

#### Virtual environment
Create a virtualenv for python 3.x, we use system-site-packages for numpy and matplotlib,
```bash
$ virtualenv --system-site-packages --python=/usr/bin/python3.x [virtualenvdir]
```

Activate the virtualenv,
```bash
$ source [virtualenvdir]/bin/activate
```

Install the required modules,
```bash
$ pip install -r requirements.txt
```

#### Configure settings
- Copy `user_settings_example.py` to `user_settings.py`.
- Configure `user_settings.py` with your system specific settings.

#### Create database
Create initial database migrations for the following apps:
- bottle
- collection
- glass
- userprofile
- whisky

```bash
$ python manage.py schemamigration <appname> --initial
```
Migrate all apps,
```bash
$ manage.py migrate <appname>
```

Run syncdb and create a Django root user,
```bash
$ python manage.py syncdb
```

#### Test run
Run test server,
```bash
$ python manage.py runserver 127.0.0.1:8000
```
