# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-29 20:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_auto_20180829_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='position_title',
            field=models.CharField(default='', max_length=40),
            preserve_default=False,
        ),
    ]