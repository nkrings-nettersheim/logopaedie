# Generated by Django 3.2.9 on 2021-12-06 07:03

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0031_alter_therapy_report_therapy_report_variation'),
    ]

    operations = [
        migrations.AddField(
            model_name='therapy_report',
            name='therapy_therapist_diagnostic',
            field=ckeditor.fields.RichTextField(default=''),
        ),
    ]