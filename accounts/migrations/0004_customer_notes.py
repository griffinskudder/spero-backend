# Generated by Django 2.1.4 on 2018-12-18 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_account_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
