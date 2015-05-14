# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('bulk', models.BooleanField(default=False)),
                ('virtual', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(null=True, to='auth.Group', blank=True)),
                ('owner', models.ForeignKey(null=True, to='userprofile.UserProfile', blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
