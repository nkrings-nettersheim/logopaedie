# Generated by Django 3.0.8 on 2021-11-22 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0023_auto_20211118_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='pa_zip_code',
            field=models.CharField(default='', max_length=10, null=True),
        ),
    ]
