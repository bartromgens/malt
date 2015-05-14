Malt
====

A Django based whisky tracker with Bootstrap web interface.

![Homepage desktop](https://github.com/bartromgens/malt/blob/master/doc/images/homescreen_desktop.png)

Dependencies
------------
- Python 3
- Django 1.8
- django-bootstrap3
- signals
- django-dual-authenticaon

Installation
-----------
#### Install numpy and matplotlib
Install the numpy and matplotlib python modules with your system package manager. These are large modules with dependencies that may not install using pip.

#### Virtual environment
Create a virtualenv for python 3.x, we use system-site-packages for numpy and matplotlib,
```bash
$ virtualenv --system-site-packages --python=/usr/bin/python3.x env
```

Activate the virtualenv,
```bash
$ source env/bin/activate
```

Install the required modules,
```bash
$ pip install -r requirements.txt
```

#### Configure settings
- Copy `user_settings_example.py` to `user_settings.py`.
- Configure `user_settings.py` with your system specific settings.

#### Create database
Create initial database:

```bash
$ python manage.py migrate
```

Create a Django root user,
```bash
$ python manage.py createsuperuser
```

#### Test run
Run test server,
```bash
$ python manage.py runserver
```

View the test server on http://127.0.0.1:8000.

Create a UserProfile for the root user via the admin before you login on the main site, http://127.0.0.1:8000/admin
