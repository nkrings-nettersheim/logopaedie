
from django.db import models


class Doctor(models.Model):
    doctor_name1 = models.CharField(max_length=50, blank=True, default='')
    doctor_name2 = models.CharField(max_length=50, blank=True, default='')
    doctor_street = models.CharField(max_length=50, blank=True, default='')
    doctor_zip_code = models.CharField(max_length=5, blank=True, default='')
    doctor_city = models.CharField(max_length=50, blank=True, default='')

    def __str__(self):
        return self.doctor_name1 + ' ' + self.doctor_name2 + '; ' + self.doctor_city



class Patient(models.Model):
    ADDRESS = (
        ('1', 'Frau'),
        ('2', 'Herr'),
        ('3', 'Firma'),
    )
    GENDER = (
        ('1', 'weiblich'),
        ('2', 'männlich'),
    )
    patient_id = models.IntegerField()
    pa_title = models.CharField(max_length=50, blank=True, default='')
    pa_address = models.CharField(max_length=1, choices=ADDRESS, default='1')
    pa_first_name = models.CharField(max_length=50)
    pa_last_name = models.CharField(max_length=50)
    pa_street = models.CharField(max_length=100)
    pa_zip_code = models.CharField(max_length=5)
    pa_city = models.CharField(max_length=255)
    pa_phone = models.CharField(max_length=20, blank=True, default='')
    pa_cell_phone = models.CharField(max_length=20, blank=True, default='')
    pa_date_of_birth = models.DateField(default='1900-01-01')
    pa_gender = models.CharField(max_length=1, choices=GENDER, default='1')
    pa_family_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return self.pa_last_name + ' ' + self.pa_first_name + '; ' + self.pa_city


class Therapy(models.Model):
    recipe_date = models.DateField(auto_now=False, auto_now_add=False)
    therapy_start = models.DateField(blank=True, default='', null=True, auto_now=False, auto_now_add=False)
    therapy_end = models.DateField(blank=True, default='', null=True, auto_now=False, auto_now_add=False)
    patients = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.recipe_date)


class Therapy_report(models.Model):
    report_date = models.DateField(blank=True, default='', null=True, auto_now=False, auto_now_add=False)
    therapy_current_result = models.TextField(default='')
    therapy_emphases = models.TextField(default='')
    therapy_forecast = models.TextField(default='')
    therapy_indication_key = models.CharField(max_length=10, default='')
    therapy_indicated = models.BooleanField(default='0')
    therapy_break = models.BooleanField(default='0')
    therapy_break_date = models.DateField(blank=True, default='', null=True, auto_now=False, auto_now_add=False)
    therapy_success = models.BooleanField(default='0')
    therapy_success_date = models.DateField(blank=True, default='', null=True, auto_now=False, auto_now_add=False)
    therapy = models.ForeignKey(Therapy, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.report_date)


class Process_report(models.Model):
    process_treatment = models.IntegerField()
    process_content = models.CharField(max_length=255)
    process_exercises = models.CharField(max_length=255)
    process_results = models.CharField(max_length=255)
    therapy = models.ForeignKey(Therapy, on_delete=models.CASCADE)

    def __str__(self):
        return self.process_content




