# Generated by Django 2.1.4 on 2018-12-25 06:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0006_auto_20181225_1313'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='assigned_users',
        ),
        migrations.AddField(
            model_name='account',
            name='assigned_users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
