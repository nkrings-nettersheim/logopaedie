# Generated by Django 2.2.3 on 2019-11-16 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0005_auto_20191116_1445'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='therapy_report',
            name='therapy_success',
        ),
        migrations.RemoveField(
            model_name='therapy_report',
            name='therapy_success_date',
        ),
        migrations.AddField(
            model_name='therapy_report',
            name='therapy_comment',
            field=models.CharField(default='', max_length=50),
        ),
    ]