# Generated by Django 2.1.4 on 2019-01-05 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20190105_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='recurringreminder',
            name='last_reminded',
            field=models.DateField(blank=True, null=True),
        ),
    ]