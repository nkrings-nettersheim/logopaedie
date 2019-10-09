# Generated by Django 2.2.3 on 2019-09-14 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0011_auto_20190914_2033'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='pa_cell_phone',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AddField(
            model_name='patient',
            name='pa_family_doctor',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='patient',
            name='pa_gender',
            field=models.CharField(choices=[('1', 'weiblich'), ('2', 'männlich')], default='1', max_length=1),
        ),
        migrations.AddField(
            model_name='patient',
            name='pa_phone',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AddField(
            model_name='patient',
            name='pa_title',
            field=models.CharField(default='', max_length=50),
        ),
    ]
