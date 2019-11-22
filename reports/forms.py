from django import forms
from .models import Patient, Therapy, Process_report, Therapy_report, Doctor


class SearchPatient(forms.Form):
    patient_id = forms.CharField(label='Patienten ID', max_length=10)

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Titel eingeben ...'
        }
    ))


class DoctorForm(forms.ModelForm):
    doctor_name1 = forms.CharField(required=True,
                                   widget=forms.TextInput(
                                       attrs={
                                           'class': 'form-control',
                                           'autofocus': 'autofocus',
                                           'placeholder': 'Name eingeben ...'
                                       }
                                   )
                                   )

    doctor_name2 = forms.CharField(required=False,
                                   widget=forms.TextInput(
                                       attrs={
                                           'class': 'form-control',
                                           'placeholder': 'Weitere Namen eingeben ...'
                                       }
                                   )
                                   )

    doctor_street = forms.CharField(required=True,
                                    widget=forms.TextInput(
                                        attrs={
                                            'class': 'form-control',
                                            'placeholder': 'Strasse eingeben ...'
                                        }
                                    )
                                    )

    doctor_zip_code = forms.CharField(required=True,
                                      widget=forms.TextInput(
                                          attrs={
                                              'class': 'form-control',
                                              'placeholder': 'PLZ eingeben ...'
                                          }
                                      )
                                      )

    doctor_city = forms.CharField(required=True,
                                  widget=forms.TextInput(
                                      attrs={
                                          'class': 'form-control',
                                          'placeholder': 'Ort eingeben ...'
                                      }
                                  )
                                  )

    class Meta:
        model = Doctor
        fields = ['doctor_name1',
                  'doctor_name2',
                  'doctor_street',
                  'doctor_zip_code',
                  'doctor_city'
                  ]


class PatientForm(forms.ModelForm):
    pa_first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Vornamen eingeben ...'
            }
        )
    )

    pa_last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'autofocus': 'autofocus',
                'placeholder': 'Nachnamen eingeben ...'
            }
        )
    )

    pa_street = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Strasse eingeben ...'
            }
        )
    )

    pa_city = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ort eingeben ...'
            }
        )
    )

    pa_phone = forms.CharField(required=False,
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control',
                                       'placeholder': 'Festnetz-Rufnummer eingeben ...'
                                   }
                               )
                               )

    pa_cell_phone = forms.CharField(required=False,
                                    widget=forms.TextInput(
                                        attrs={
                                            'class': 'form-control',
                                            'placeholder': 'Mobilfunk-Rufnummer eingeben ...'
                                        }
                                    )
                                    )

    pa_date_of_birth = forms.DateField(required=True,
                                       widget=forms.DateInput(
                                           attrs={
                                               'class': 'form-control',
                                               'placeholder': 'Geburtsdatum eingeben ...'
                                           }
                                       )
                                       )

    GENDER = (
        ('1', 'weiblich'),
        ('2', 'männlich'),
    )

    pa_gender = forms.ChoiceField(choices=GENDER, label="", initial=1, widget=forms.Select(
        attrs={
            'class': 'form-control'
        }
    ))

    pa_family_doctor = forms.ModelChoiceField(queryset=Doctor.objects.all())

    class Meta:
        model = Patient
        fields = ['pa_first_name',
                  'pa_last_name',
                  'pa_street',
                  'pa_city',
                  'pa_phone',
                  'pa_cell_phone',
                  'pa_date_of_birth',
                  'pa_gender',
                  'pa_family_doctor'
                  ]


class TherapyForm(forms.ModelForm):
    recipe_date = forms.DateField(required=True,
                                  widget=forms.DateInput(
                                      attrs={
                                          'class': 'form-control',
                                          'autofocus': 'autofocus',
                                          'placeholder': 'Rezeptdatum eingeben ...'
                                      }
                                  )
                                  )

    therapy_start = forms.DateField(required=False,
                                    widget=forms.DateInput(
                                        attrs={
                                            'class': 'form-control',
                                            'placeholder': 'Start der Therapie ...'
                                        }
                                    )
                                    )

    therapy_end = forms.DateField(required=False,
                                  widget=forms.DateInput(
                                      attrs={
                                          'class': 'form-control',
                                          'placeholder': 'Ende der Therapie ...'
                                      }
                                  )
                                  )

    therapy_regulation_amount = forms.IntegerField(required=False,
                                                   widget=forms.NumberInput(
                                                   )
                                                   )

    therapy_duration = forms.CharField(required=False,
                                       widget=forms.TextInput(
                                           attrs={
                                               'class': 'form-control',
                                               'placeholder': 'Therapiedauer ...'
                                           }
                                       )
                                       )

    INDICATION = (
        ('ST1', 'ST1'),
        ('ST2', 'ST2'),
        ('ST3', 'ST3'),
        ('ST4', 'ST4'),
        ('SP1', 'SP1'),
        ('SP2', 'SP2'),
        ('SP3', 'SP3'),
        ('SP4', 'SP4'),
        ('SP5', 'SP5'),
        ('SP6', 'SP6'),
        ('RE1', 'RE1'),
        ('RE2', 'RE2'),
        ('SF', 'SF'),
        ('SC1', 'SC1'),
        ('SC2', 'SC2'),
    )

    therapy_indication_key = forms.ChoiceField(choices=INDICATION, label="", initial=1, widget=forms.Select(
        attrs={
            'class': 'form-control'
        }
    ))

    therapy_icd_cod = forms.CharField(required=False,
                                      widget=forms.TextInput(
                                          attrs={
                                              'class': 'form-control',
                                              'placeholder': 'ICD-CoD eingeben ...'
                                          }
                                      )
                                      )

    therapy_doctor = forms.ModelChoiceField(queryset=Doctor.objects.all())

    patients = forms.ModelChoiceField(queryset=Patient.objects.all())

    class Meta:
        model = Therapy
        fields = ['recipe_date',
                  'therapy_start',
                  'therapy_end',
                  'therapy_regulation_amount',
                  'therapy_duration',
                  'therapy_indication_key',
                  'therapy_icd_cod',
                  'therapy_doctor',
                  'patients']


class ProcessReportForm(forms.ModelForm):
    process_treatment = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control-plaintext',
            'readonly': ''
        }
    )
    )

    process_content = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'cols': '20',
            'rows': '5'
        }
    ))

    class Meta:
        model = Process_report
        fields = ['process_treatment',
                  'process_content',
                  'process_exercises',
                  'process_results',
                  'therapy'
                  ]


class TherapyReportForm(forms.ModelForm):
    report_date = forms.DateField(required=False,
                                  widget=forms.DateInput(
                                      attrs={
                                          'class': 'form-control',
                                          'autofocus': 'autofocus',
                                          'placeholder': 'Report Datum festlegen ...'
                                      }
                                  )
                                  )

    therapy_current_result = forms.CharField(required=False,
                                             max_length=500,
                                             widget=forms.Textarea(
                                                 attrs={
                                                     'class': 'form-control',
                                                     'cols': '20',
                                                     'rows': '5'
                                                 }
                                             ))

    therapy_emphases = forms.CharField(required=False,
                                       max_length=500,
                                       widget=forms.Textarea(
                                           attrs={
                                               'class': 'form-control',
                                               'cols': '20',
                                               'rows': '5'
                                           }
                                       ))

    therapy_forecast = forms.CharField(required=False,
                                       max_length=500,
                                       widget=forms.Textarea(
                                           attrs={
                                               'class': 'form-control',
                                               'cols': '20',
                                               'rows': '5'
                                           }
                                       ))

    INDICATION = (
        ('ST1', 'ST1'),
        ('ST2', 'ST2'),
        ('ST3', 'ST3'),
        ('ST4', 'ST4'),
        ('SP1', 'SP1'),
        ('SP2', 'SP2'),
        ('SP3', 'SP3'),
        ('SP4', 'SP4'),
        ('SP5', 'SP5'),
        ('SP6', 'SP6'),
        ('RE1', 'RE1'),
        ('RE2', 'RE2'),
        ('SF', 'SF'),
        ('SC1', 'SC1'),
        ('SC2', 'SC2'),
    )

    therapy_indication_key = forms.ChoiceField(choices=INDICATION, label="", initial=1, widget=forms.Select(
        attrs={
            'class': 'form-control'
        }
    ))

    therapy_indicated = forms.NullBooleanField()

    therapy_break = forms.NullBooleanField()

    therapy_break_date = forms.DateField(required=False,
                                         widget=forms.DateInput(
                                             attrs={
                                                 'class': 'form-control',
                                                 'placeholder': 'Datum festlegen ...'
                                             }
                                         )
                                         )

    therapy_comment = forms.CharField(required=False,
                                       widget=forms.TextInput(
                                           attrs={
                                               'class': 'form-control',
                                               'placeholder': 'Bemerkung ...'
                                           }
                                       )
                                       )

    class Meta:
        model = Therapy_report
        fields = ['report_date',
                  'therapy_current_result',
                  'therapy_emphases',
                  'therapy_forecast',
                  'therapy_indication_key',
                  'therapy_indicated',
                  'therapy_break',
                  'therapy_break_date',
                  'therapy_comment',
                  'therapy']
