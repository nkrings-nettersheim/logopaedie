# Generated by Django 2.2.3 on 2019-12-08 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0015_therapy_therapy_report_no_yes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='therapy',
            name='therapy_report_no_yes',
            field=models.BooleanField(default=True),
        ),
    ]
