# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Distillery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('lat', models.FloatField(default='0.0', verbose_name='latitude')),
                ('lon', models.FloatField(default='0.0', verbose_name='longitude')),
                ('url', models.URLField(max_length=400, default='', blank=True)),
                ('image', models.URLField(max_length=400, default='', blank=True)),
                ('sound', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('lat', models.FloatField(default='0.0', verbose_name='latitude')),
                ('lon', models.FloatField(default='0.0', verbose_name='longitude')),
                ('date', models.DateTimeField(default=datetime.datetime.now, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Whisky',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('age', models.FloatField(verbose_name='age')),
                ('alcoholPercentage', models.FloatField(verbose_name='alcohol %')),
                ('url', models.URLField(max_length=400, default='', blank=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('distillery', models.ForeignKey(to='whisky.Distillery')),
            ],
            options={
                'ordering': ['distillery'],
            },
        ),
        migrations.AddField(
            model_name='distillery',
            name='region',
            field=models.ForeignKey(to='whisky.Region'),
        ),
    ]
