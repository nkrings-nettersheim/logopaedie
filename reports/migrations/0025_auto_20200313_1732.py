# Generated by Django 3.0.1 on 2020-03-13 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0024_patient_something'),
    ]

    operations = [
        migrations.AlterField(
            model_name='therapy_report',
            name='therapy_comment',
            field=models.CharField(default='', max_length=255),
        ),
    ]
