# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bottle', '0001_initial'),
        ('collection', '0001_initial'),
        ('whisky', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bottle',
            name='collection',
            field=models.ForeignKey(null=True, to='collection.Collection', blank=True),
        ),
        migrations.AddField(
            model_name='bottle',
            name='whisky',
            field=models.ForeignKey(null=False, to='whisky.Whisky', blank=False),
        ),
    ]
