# Generated by Django 2.2.3 on 2019-09-14 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0013_auto_20190914_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='pa_cell_phone',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='patient',
            name='pa_family_doctor',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='patient',
            name='pa_phone',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='patient',
            name='pa_title',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
