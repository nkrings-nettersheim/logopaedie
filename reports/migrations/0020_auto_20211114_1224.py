# Generated by Django 3.0.8 on 2021-11-14 11:24

from django_ckeditor_5.fields import CKEditor5Field
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0019_auto_20211109_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wait_list',
            name='wl_information',
            field=CKEditor5Field(),
            preserve_default=False,
        ),
    ]
