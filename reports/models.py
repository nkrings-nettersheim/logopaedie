import os
#from datetime import date, timezone
#from django.utils import timezone
from datetime import datetime

from django.db import models
from ckeditor.fields import RichTextField


class Doctor(models.Model):
    doctor_name1 = models.CharField(max_length=75, blank=True, default='')
    doctor_name2 = models.CharField(max_length=75, blank=True, default='')
    doctor_name3 = models.CharField(max_length=75, blank=True, default='')
    doctor_street = models.CharField(max_length=50, blank=True, default='')
    doctor_zip_code = models.CharField(max_length=5, blank=True, default='')
    doctor_city = models.CharField(max_length=50, blank=True, default='')
    doctor_lanr = models.CharField(max_length=9, blank=False, unique=True, default='')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.doctor_lanr


class Therapist(models.Model):
    tp_first_name = models.CharField(max_length=50, blank=True, default='')
    tp_last_name = models.CharField(max_length=50, blank=True, default='')
    tp_initial = models.CharField(max_length=5, blank=True, default='')
    tp_user_logopakt = models.CharField(max_length=20, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.tp_initial

class Diagnostic_group(models.Model):
    diagnostic_key = models.CharField(max_length=10, default=True, unique=True)
    diagnostic_description = models.CharField(max_length=250, default=False)
    diagnostic_max_therapy = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.diagnostic_key


class Patient(models.Model):
    GENDER = (
        ('1', 'weiblich'),
        ('2', 'männlich'),
    )
    pa_first_name = models.CharField(max_length=50)
    pa_last_name = models.CharField(max_length=50)
    pa_street = models.CharField(max_length=100)
    pa_zip_code = models.CharField(max_length=10, default='')
    pa_city = models.CharField(max_length=255)
    pa_phone = models.CharField(max_length=100, blank=True, default='', null=True)
    pa_cell_phone = models.CharField(max_length=100, blank=True, default='', null=True)
    pa_cell_phone_add1 = models.CharField(max_length=100, blank=True, default='', null=True)
    pa_cell_phone_add2 = models.CharField(max_length=100, blank=True, default='', null=True)
    pa_cell_phone_sms = models.CharField(max_length=100, blank=True, default='', null=True)
    pa_email = models.EmailField(max_length=254, blank=True)
    pa_date_of_birth = models.DateField(default='1900-01-01')
    pa_gender = models.CharField(max_length=1, choices=GENDER, default='1')
    pa_attention = models.CharField(max_length=100, blank=True, default='')
    pa_allergy = models.CharField(max_length=100, blank=True, default='')
    pa_note = models.CharField(max_length=255, blank=True, default='')
    pa_active_no_yes = models.BooleanField(default=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)


    def __str__(self):
        return self.pa_last_name + ' ' + self.pa_first_name + '; ' + self.pa_city

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['pa_first_name', 'pa_last_name', 'pa_date_of_birth'], name='unique pa_name'),
        ]


class Therapy(models.Model):
    recipe_date = models.DateField(auto_now=False, auto_now_add=False)
    therapy_regulation_amount = models.IntegerField(blank=True, null=True)
    therapy_duration = models.CharField(max_length=10, default='')
    therapy_frequence = models.CharField(max_length=5, default='')
    therapy_rid_of = models.BooleanField(default=False, null=True)
    therapy_report_no_yes = models.BooleanField(default=True, null=True)
    therapy_homevisit_no_yes = models.BooleanField(default=False, null=True)
    therapy_indication_key = models.CharField(max_length=10, default='')
    therapy_icd_cod = models.CharField(max_length=10, default='')
    therapy_icd_cod_2 = models.CharField(max_length=10, default='')
    therapy_icd_cod_3 = models.CharField(max_length=10, default='')
    therapy_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, default='')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    patients = models.ForeignKey(Patient, on_delete=models.CASCADE, default='')
    therapists = models.ForeignKey(Therapist, on_delete=models.PROTECT, default='', null=True)
    diagnostic_group = models.ForeignKey(Diagnostic_group, on_delete=models.PROTECT, default='1', null=True)
    first_diagnostic_no_yes = models.BooleanField(default=False, null=True)
    need_diagnostic_no_yes = models.BooleanField(default=False, null=True)

    def __str__(self):
        return str(self.recipe_date)

    def save(self, force_insert=False, force_update=False):
        self.therapy_icd_cod = self.therapy_icd_cod.upper()
        super(Therapy, self).save(force_insert, force_update)


class Therapy_report(models.Model):
    report_date = models.DateField(blank=True, default='', null=True, auto_now=False, auto_now_add=False)
    therapy_start = models.DateField(blank=True, default=None, null=True, auto_now=False, auto_now_add=False)
    therapy_end = models.DateField(blank=True, default=None, null=True, auto_now=False, auto_now_add=False)
    therapy_current_result = RichTextField()
    therapy_emphases = RichTextField()
    therapy_forecast = RichTextField()
    therapy_indicated = models.BooleanField(default=False)
    therapy_break = models.BooleanField(default=False)
    therapy_break_date = models.DateField(blank=True, default='', null=True, auto_now=False, auto_now_add=False)
    therapy_comment = models.CharField(max_length=255, default='')
    therapy = models.ForeignKey(Therapy, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    therapy_individual = models.BooleanField(default=False)
    therapy_individual_min = models.IntegerField(default=0)
    therapy_group = models.BooleanField(default=False)
    therapy_group_min = models.IntegerField(default=0)
    therapy_finish = models.BooleanField(default=False)
    therapy_re_introduction = models.BooleanField(default=False)
    therapy_re_introduction_weeks = models.IntegerField(default=0)
    therapy_frequence = models.BooleanField(default=False)
    therapy_frequence_count_per_week = models.IntegerField(default=0)
    therapy_another = models.BooleanField(default=False)
    therapy_another_text = models.CharField(max_length=25, default='')
    therapy_home_visit = models.BooleanField(default=False)

    def __str__(self):
        return str(self.report_date)


class Process_report(models.Model):
    process_treatment = models.IntegerField(default=0)
    process_content = models.CharField(max_length=255, blank=True, default='')
    process_exercises = models.CharField(max_length=255, blank=True, default='')
    process_results = models.CharField(max_length=50, blank=True, default='')
    process_content_2 = models.CharField(max_length=255, blank=True, default='')
    process_exercises_2 = models.CharField(max_length=255, blank=True, default='')
    process_results_2 = models.CharField(max_length=50, blank=True, default='')
    process_content_3 = models.CharField(max_length=255, blank=True, default='')
    process_exercises_3 = models.CharField(max_length=255, blank=True, default='')
    process_results_3 = models.CharField(max_length=50, blank=True, default='')
    therapy = models.ForeignKey(Therapy, on_delete=models.CASCADE, default='')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.process_content


class InitialAssessment(models.Model):
    RESULT = (
        ('1', 'sehr gut'),
        ('2', 'gut'),
        ('3', 'befriedigend'),
        ('4', 'schlecht'),
        ('5', 'sehr schlecht'),
        ('6', 'nicht auswertbar')
    )

    ia_date = models.DateField(blank=True, default='', null=True, auto_now=False, auto_now_add=False)
    ia_assessment = models.CharField(max_length=100, blank=True, default='')
    ia_artikulation = models.CharField(max_length=100, blank=True, default='')
    ia_dysphagie = models.CharField(max_length=100, blank=True, default='')
    ia_syntax = models.CharField(max_length=100, blank=True, default='')
    ia_semantik = models.CharField(max_length=100, blank=True, default='')
    ia_understanding = models.CharField(max_length=100, blank=True, default='')
    ia_expiration = models.CharField(max_length=100, blank=True, default='')
    ia_motor_skills = models.CharField(max_length=100, blank=True, default='')
    ia_perception = models.CharField(max_length=100, blank=True, default='')
    ia_breathing = models.CharField(max_length=100, blank=True, default='')
    ia_other = models.CharField(max_length=100, blank=True, default='')
    ia_test = models.CharField(max_length=100, blank=True, default='')
    ia_test_date = models.DateField(blank=True, default='', null=True, auto_now=False, auto_now_add=False)
    ia_test_result = models.CharField(max_length=1, choices=RESULT, default='1')
    ia_enhancement = models.BooleanField(default=False, null=True)
    ia_information = models.CharField(max_length=500, blank=True, default='')
    ia_first_diagnostic = RichTextField(blank=True, null=True)
    therapy = models.ForeignKey(Therapy, on_delete=models.CASCADE, default='')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.ia_assessment


def dynamik_path(instance, filename):
    file_path = 'patient/{patient_id}/{filename}'.format(patient_id=instance.patient_id, filename=filename)
    return file_path


class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to=dynamik_path, max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, default='')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)


def dynamik_path_therapy(instance, filename):
    file_path = 'therapy/{therapy_id}/{filename}'.format(therapy_id=instance.therapy_id, filename=filename)
    return file_path


class Document_therapy(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to=dynamik_path_therapy, max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    therapy = models.ForeignKey(Therapy, on_delete=models.CASCADE, default='')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)


class Therapy_Something(models.Model):
    something_else = RichTextField()
    therapy = models.ForeignKey(Therapy, on_delete=models.CASCADE, default='')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)


class Patient_Something(models.Model):
    pa_something_else = RichTextField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, default='')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

class Login_Failed(models.Model):
    ipaddress = models.CharField(max_length=100, blank=True, default='')
    user_name = models.CharField(max_length=100, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
