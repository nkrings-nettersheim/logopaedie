# Generated by Django 3.0.8 on 2021-01-15 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0014_auto_20210115_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='therapy_report',
            name='therapy_necessary',
            field=models.BooleanField(default=False),
        ),
    ]
