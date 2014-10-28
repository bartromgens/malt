#!/bin/bash

python manage.py schemamigration bottle --auto
python manage.py migrate bottle

python manage.py schemamigration collection --auto
python manage.py migrate collection

python manage.py schemamigration glass --auto
python manage.py migrate glass

python manage.py schemamigration userprofile --auto
python manage.py migrate userprofile

python manage.py schemamigration whisky --auto
python manage.py migrate whisky
