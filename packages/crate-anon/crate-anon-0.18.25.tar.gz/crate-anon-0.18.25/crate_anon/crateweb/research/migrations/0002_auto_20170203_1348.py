# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-03 13:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queryaudit',
            name='n_records',
            field=models.IntegerField(default=0),
        ),
    ]
