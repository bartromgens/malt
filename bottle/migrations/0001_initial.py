# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bottle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('volume', models.FloatField(default=700.0, verbose_name='volume')),
                ('volumeConsumedInitial', models.FloatField(default=0.0, verbose_name='initially consumed')),
                ('empty', models.BooleanField(default=False)),
                ('price', models.FloatField(default=0.0, verbose_name='price')),
                ('donation', models.BooleanField(default=False)),
                ('date', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('buyer', models.ForeignKey(default=1, to='userprofile.UserProfile')),
            ],
            options={
                'ordering': ['whisky'],
            },
        ),
    ]
