# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-26 18:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20171226_1810'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sub',
            old_name='lisert',
            new_name='picks',
        ),
    ]
