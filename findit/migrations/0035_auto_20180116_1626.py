# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-16 16:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('findit', '0034_tips'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tips',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='tips',
            name='image_1',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]