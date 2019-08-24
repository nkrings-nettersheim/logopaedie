import datetime

from django.db import models
from django.utils import timezone


class Patient(models.Model):
    ADDRESS = (
        ('1', 'Frau'),
        ('2', 'Herr'),
        ('3', 'Firma'),
    )
    patient_id = models.IntegerField()
    pa_address = models.CharField(max_length=1, choices=ADDRESS, default='1')
    pa_first_name = models.CharField(max_length=50)
    pa_geburtsdatum = models.CharField(max_length=255)
    pa_last_name = models.CharField(max_length=50)
    pa_street = models.CharField(max_length=100)
    pa_zip_code = models.CharField(max_length=5)
    pa_city = models.CharField(max_length=255)


    def __str__(self):
        return self.pa_last_name


class Process_report(models.Model):
    report_date = models.CharField(max_length=8)
    diagnostic_1 = models.CharField(max_length=255)
    diagonstic_2 = models.CharField(max_length=255)
    patients = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return self.report_date


class Therapy(models.Model):
    recipe_date = models.DateField(auto_now=False, auto_now_add=False)
    therapy_start = models.DateField(auto_now=False, auto_now_add=False)
    therapy_end = models.DateField(auto_now=False, auto_now_add=False)
    patients = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.recipe_date)


class Therapy_report(models.Model):
    therapy_treatment = models.IntegerField()
    therapy_content = models.CharField(max_length=255)
    therapy_exercises = models.CharField(max_length=255)
    therapy_results = models.CharField(max_length=255)
    therapy = models.ForeignKey(Therapy, on_delete=models.CASCADE)

    def __str__(self):
        return self.therapy_content




class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    #    def was_published_recently(self):
    #        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
