# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-30 14:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_position_position_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='user',
            new_name='owner',
        ),
    ]
