# Generated by Django 3.0.8 on 2021-11-29 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0024_auto_20211122_2251'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shortcuts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short', models.CharField(max_length=10)),
                ('long', models.CharField(blank=True, default='', max_length=200, null=True)),
            ],
        ),
    ]
