# Generated by Django 2.1.4 on 2018-12-18 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_customer_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reminder',
            name='alert_time',
            field=models.DateField(blank=True, null=True),
        ),
    ]