# Generated by Django 3.0.1 on 2020-01-25 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0016_patient_pa_allergy'),
    ]

    operations = [
        migrations.AddField(
            model_name='therapy',
            name='therapy_homevisit_no_yes',
            field=models.BooleanField(default=False, null=True),
        ),
    ]