# Generated by Django 2.0.3 on 2018-03-22 23:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sub',
            name='user',
            field=models.ForeignKey(on_delete=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
