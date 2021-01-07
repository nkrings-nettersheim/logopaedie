# Generated by Django 3.0.8 on 2021-01-06 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0010_therapy_continue_diagnostic_no_yes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='therapy_report',
            name='therapy_break_date',
        ),
        migrations.AddField(
            model_name='therapy_report',
            name='therapy_re_introduction',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='therapy_report',
            name='therapy_re_introduction_weeks',
            field=models.IntegerField(default=0),
        ),
    ]
