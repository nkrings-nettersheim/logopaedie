# Generated by Django 3.0.8 on 2020-12-26 15:29

from django_ckeditor_5.fields import CKEditor5Field
from django.db import migrations, models
import django.db.models.deletion
import reports.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Diagnostic_group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnostic_key', models.CharField(default=True, max_length=10, unique=True)),
                ('diagnostic_description', models.CharField(default=False, max_length=250)),
                ('diagnostic_max_therapy', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor_name1', models.CharField(blank=True, default='', max_length=75)),
                ('doctor_name2', models.CharField(blank=True, default='', max_length=75)),
                ('doctor_name3', models.CharField(blank=True, default='', max_length=75)),
                ('doctor_street', models.CharField(blank=True, default='', max_length=50)),
                ('doctor_zip_code', models.CharField(blank=True, default='', max_length=5)),
                ('doctor_city', models.CharField(blank=True, default='', max_length=50)),
                ('doctor_lanr', models.CharField(default='', max_length=9, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('document', models.FileField(upload_to=reports.models.dynamik_path)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Document_therapy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('document', models.FileField(upload_to=reports.models.dynamik_path_therapy)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='InitialAssessment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ia_date', models.DateField(blank=True, default='', null=True)),
                ('ia_assessment', models.CharField(blank=True, default='', max_length=100)),
                ('ia_artikulation', models.CharField(blank=True, default='', max_length=100)),
                ('ia_dysphagie', models.CharField(blank=True, default='', max_length=100)),
                ('ia_syntax', models.CharField(blank=True, default='', max_length=100)),
                ('ia_semantik', models.CharField(blank=True, default='', max_length=100)),
                ('ia_understanding', models.CharField(blank=True, default='', max_length=100)),
                ('ia_expiration', models.CharField(blank=True, default='', max_length=100)),
                ('ia_motor_skills', models.CharField(blank=True, default='', max_length=100)),
                ('ia_perception', models.CharField(blank=True, default='', max_length=100)),
                ('ia_breathing', models.CharField(blank=True, default='', max_length=100)),
                ('ia_other', models.CharField(blank=True, default='', max_length=100)),
                ('ia_test', models.CharField(blank=True, default='', max_length=100)),
                ('ia_test_date', models.DateField(blank=True, default='', null=True)),
                ('ia_test_result', models.CharField(choices=[('1', 'sehr gut'), ('2', 'gut'), ('3', 'befriedigend'), ('4', 'schlecht'), ('5', 'sehr schlecht'), ('6', 'nicht auswertbar')], default='1', max_length=1)),
                ('ia_enhancement', models.BooleanField(default=False, null=True)),
                ('ia_information', models.CharField(blank=True, default='', max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Login_Failed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ipaddress', models.CharField(blank=True, default='', max_length=100)),
                ('user_name', models.CharField(blank=True, default='', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pa_first_name', models.CharField(max_length=50)),
                ('pa_last_name', models.CharField(max_length=50)),
                ('pa_street', models.CharField(max_length=100)),
                ('pa_zip_code', models.CharField(default='', max_length=10)),
                ('pa_city', models.CharField(max_length=255)),
                ('pa_phone', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('pa_cell_phone', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('pa_cell_phone_add1', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('pa_cell_phone_add2', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('pa_cell_phone_sms', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('pa_email', models.EmailField(blank=True, max_length=254)),
                ('pa_date_of_birth', models.DateField(default='1900-01-01')),
                ('pa_gender', models.CharField(choices=[('1', 'weiblich'), ('2', 'männlich')], default='1', max_length=1)),
                ('pa_attention', models.CharField(blank=True, default='', max_length=100)),
                ('pa_allergy', models.CharField(blank=True, default='', max_length=100)),
                ('pa_note', models.CharField(blank=True, default='', max_length=255)),
                ('pa_active_no_yes', models.BooleanField(default=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Therapist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tp_first_name', models.CharField(blank=True, default='', max_length=50)),
                ('tp_last_name', models.CharField(blank=True, default='', max_length=50)),
                ('tp_initial', models.CharField(blank=True, default='', max_length=5)),
                ('tp_user_logopakt', models.CharField(blank=True, default='', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Therapy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe_date', models.DateField()),
                ('therapy_regulation_amount', models.IntegerField(blank=True, null=True)),
                ('therapy_duration', models.CharField(default='', max_length=10)),
                ('therapy_frequence', models.CharField(default='', max_length=5)),
                ('therapy_rid_of', models.BooleanField(default=False, null=True)),
                ('therapy_report_no_yes', models.BooleanField(default=True, null=True)),
                ('therapy_homevisit_no_yes', models.BooleanField(default=False, null=True)),
                ('therapy_indication_key', models.CharField(default='', max_length=10)),
                ('therapy_icd_cod', models.CharField(default='', max_length=10)),
                ('therapy_icd_cod_2', models.CharField(default='', max_length=10)),
                ('therapy_icd_cod_3', models.CharField(default='', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('diagnostic_group', models.ForeignKey(default='1', null=True, on_delete=django.db.models.deletion.PROTECT, to='reports.Diagnostic_group')),
                ('patients', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='reports.Patient')),
                ('therapists', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.PROTECT, to='reports.Therapist')),
                ('therapy_doctor', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='reports.Doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Therapy_Something',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('something_else', CKEditor5Field()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('therapy', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='reports.Therapy')),
            ],
        ),
        migrations.CreateModel(
            name='Therapy_report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_date', models.DateField(blank=True, default='', null=True)),
                ('therapy_start', models.DateField(blank=True, default=None, null=True)),
                ('therapy_end', models.DateField(blank=True, default=None, null=True)),
                ('therapy_current_result', CKEditor5Field()),
                ('therapy_emphases', CKEditor5Field()),
                ('therapy_forecast', CKEditor5Field()),
                ('therapy_indicated', models.BooleanField(default=False)),
                ('therapy_break', models.BooleanField(default=False)),
                ('therapy_break_date', models.DateField(blank=True, default='', null=True)),
                ('therapy_comment', models.CharField(default='', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('therapy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.Therapy')),
            ],
        ),
        migrations.CreateModel(
            name='Process_report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_treatment', models.IntegerField(default=0)),
                ('process_content', models.CharField(blank=True, default='', max_length=255)),
                ('process_exercises', models.CharField(blank=True, default='', max_length=255)),
                ('process_results', models.CharField(blank=True, default='', max_length=50)),
                ('process_content_2', models.CharField(blank=True, default='', max_length=255)),
                ('process_exercises_2', models.CharField(blank=True, default='', max_length=255)),
                ('process_results_2', models.CharField(blank=True, default='', max_length=50)),
                ('process_content_3', models.CharField(blank=True, default='', max_length=255)),
                ('process_exercises_3', models.CharField(blank=True, default='', max_length=255)),
                ('process_results_3', models.CharField(blank=True, default='', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('therapy', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='reports.Therapy')),
            ],
        ),
        migrations.CreateModel(
            name='Patient_Something',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pa_something_else', CKEditor5Field()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('patient', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='reports.Patient')),
            ],
        ),
        migrations.AddConstraint(
            model_name='patient',
            constraint=models.UniqueConstraint(fields=('pa_first_name', 'pa_last_name', 'pa_date_of_birth'), name='unique pa_name'),
        ),
        migrations.AddField(
            model_name='initialassessment',
            name='therapy',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='reports.Therapy'),
        ),
        migrations.AddField(
            model_name='document_therapy',
            name='therapy',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='reports.Therapy'),
        ),
        migrations.AddField(
            model_name='document',
            name='patient',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='reports.Patient'),
        ),
    ]
