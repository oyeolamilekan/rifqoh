# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-28 19:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0016_auto_20171226_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='querylist',
            name='baser_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]