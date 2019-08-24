from django import forms
from .models import Patient, Therapy, Therapy_report


class SearchPatient(forms.Form):
    patient_id = forms.CharField(label='Patienten ID', max_length=10)


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['pa_address', 'patient_id','pa_first_name', 'pa_last_name', 'pa_street', 'pa_zip_code', 'pa_city']


class TherapyForm(forms.ModelForm):
    class Meta:
        model = Therapy
        fields = ['recipe_date', 'therapy_start','therapy_end', 'patients']


class TherapyReportForm(forms.ModelForm):
    class Meta:
        model = Therapy_report
        fields = ['therapy_treatment','therapy_content', 'therapy_exercises', 'therapy_results', 'therapy']
