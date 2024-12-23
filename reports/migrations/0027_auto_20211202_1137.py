# Generated by Django 3.2.9 on 2021-12-02 10:37

from django_ckeditor_5.fields import CKEditor5Field
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0026_alter_wait_list_wl_information'),
    ]

    operations = [
        migrations.AddField(
            model_name='therapy_report',
            name='therapy_aims',
            field=CKEditor5Field(),
        ),
        migrations.AddField(
            model_name='therapy_report',
            name='therapy_compliance',
            field=CKEditor5Field(),
        ),
        migrations.AddField(
            model_name='therapy_report',
            name='therapy_content',
            field=CKEditor5Field(),
        ),
        migrations.AddField(
            model_name='therapy_report',
            name='therapy_diagnostic',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='therapy_report',
            name='therapy_doc_diagnostic',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='therapy_report',
            name='therapy_insurance',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='therapy_report',
            name='therapy_process',
            field=CKEditor5Field(),
        ),
        migrations.AddField(
            model_name='therapy_report',
            name='therapy_request_of',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='therapy_report',
            name='therapy_status',
            field=CKEditor5Field(),
        ),
        migrations.AddField(
            model_name='therapy_report',
            name='therapy_summary',
            field=CKEditor5Field(),
        ),
    ]
