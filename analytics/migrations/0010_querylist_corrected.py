# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-03 09:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0009_auto_20171119_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='querylist',
            name='corrected',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
