# Generated by Django 2.0.4 on 2018-06-12 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('findit', '0007_products_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='feelings',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]