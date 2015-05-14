# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('bottle', '0001_initial'),
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Glass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('mass', models.FloatField(default=0.0, verbose_name='mass', blank=True)),
                ('volume', models.FloatField(default=50.0, verbose_name='volume')),
                ('rating', models.IntegerField(default=-1, blank=True)),
                ('date', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('bottle', models.ForeignKey(to='bottle.Bottle')),
                ('user', models.ForeignKey(to='userprofile.UserProfile')),
            ],
        ),
    ]
