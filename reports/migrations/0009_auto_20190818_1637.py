# Generated by Django 2.2.3 on 2019-08-18 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0008_auto_20190818_1114'),
    ]

    operations = [
        migrations.RenameField(
            model_name='therapy_report',
            old_name='treatment',
            new_name='therapy_treatment',
        ),
        migrations.RemoveField(
            model_name='therapy_report',
            name='report_date',
        ),
    ]
