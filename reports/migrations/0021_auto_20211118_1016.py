# Generated by Django 3.0.8 on 2021-11-18 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0020_auto_20211114_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='wait_list',
            name='wl_old',
            field=models.CharField(blank=True, default='', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='wait_list',
            name='wl_date_of_birth',
            field=models.DateField(default='1900-01-01'),
        ),
    ]
