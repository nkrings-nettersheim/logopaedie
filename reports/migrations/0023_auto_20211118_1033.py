# Generated by Django 3.0.8 on 2021-11-18 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0022_auto_20211118_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wait_list',
            name='wl_date_of_birth',
            field=models.DateField(blank=True, default='1900-01-01', null=True),
        ),
    ]
