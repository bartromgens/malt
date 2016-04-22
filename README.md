Malt
====
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/bartromgens/malt/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/bartromgens/malt/?branch=master)  
A whisky collection administration and drink tracking web application based on Django and Bootstrap.

![Homepage desktop](https://github.com/bartromgens/malt/blob/master/doc/images/homescreen_desktop.png)

Dependencies
------------
- Python 3
- Django 1.8
- numpy
- matplotlib
- django-bootstrap3
- django-dual-authenticaon
- signals

Installation
-----------
#### Install numpy and matplotlib
Install the numpy and matplotlib python modules with your system package manager. These are large modules with dependencies that may not install using pip.

#### Virtual environment
Create a virtualenv for python 3.x,
```bash
$ virtualenv --python=/usr/bin/python3.x env
```

Activate the virtualenv,
```bash
$ source env/bin/activate
```

Install the required packages,
```bash
$ pip install -r requirements.txt
```

#### Configure settings
Generate a local settings file from the example local settings,
```bash
$ python create_local_settings.py
```
And change the settings in `local_settings.py` to your local environment.

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
