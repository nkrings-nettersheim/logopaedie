# Generated by Django 3.2.9 on 2022-06-24 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0035_auto_20220623_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='parents_form',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='document',
            name='registration_form',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
