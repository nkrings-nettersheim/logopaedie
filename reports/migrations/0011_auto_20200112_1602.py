# Generated by Django 3.0.1 on 2020-01-12 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0010_doctor_doctor_name3'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='doctor_lanr',
            field=models.CharField(default='', max_length=9, unique=True),
        ),
    ]