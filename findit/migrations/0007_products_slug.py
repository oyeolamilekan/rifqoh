# Generated by Django 2.0.3 on 2018-03-27 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('findit', '0006_auto_20180323_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]