# Generated by Django 3.2.9 on 2021-12-05 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0030_alter_therapy_report_therapy_report_variation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='therapy_report',
            name='therapy_report_variation',
            field=models.IntegerField(default=1),
        ),
    ]