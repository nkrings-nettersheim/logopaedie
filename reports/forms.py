from django import forms
from .models import Patient, Therapy, Therapy_report


class SearchPatient(forms.Form):
    patient_id = forms.CharField(label='Patienten ID', max_length=10)


class PatientForm(forms.ModelForm):
    pa_title = forms.CharField(required=False,
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control',
                                       'placeholder': 'Titel eingeben ...'
                                   }
                               )
                               )

    ADDRESS = (
        ('1', 'Frau'),
        ('2', 'Herr'),
        ('3', 'Firma'),
    )

    pa_address = forms.ChoiceField(choices=ADDRESS, label="", initial=1, widget=forms.Select(
        attrs={
            'class': 'form-control'
        }
    ))

    patient_id = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Interne Patienten-Nr. eingeben ...'
            }
        )
    )

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

    pa_zip_code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'PLZ eingeben ...'
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

    pa_date_of_birth = forms.DateField(required=False,
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

    pa_family_doctor = forms.CharField(required=False,
                                       widget=forms.TextInput(
                                           attrs={
                                               'class': 'form-control',
                                               'placeholder': 'Hausarzt eingeben ...'
                                           }
                                       )
                                       )

    class Meta:
        model = Patient
        fields = ['pa_title',
                  'pa_address',
                  'patient_id',
                  'pa_first_name',
                  'pa_last_name',
                  'pa_street',
                  'pa_zip_code',
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

    patients = forms.ModelChoiceField(queryset=Patient.objects.all())

    class Meta:
        model = Therapy
        fields = ['recipe_date',
                  'therapy_start',
                  'therapy_end',
                  'patients'
                  ]


class TherapyReportForm(forms.ModelForm):
    therapy_treatment = forms.CharField(widget=forms.TextInput(
                                      attrs={
                                          'class': 'form-control-plaintext',
                                          'readonly': ''
                                      }
                                  )
    )

    therapy_content = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'cols': '20',
            'rows': '5'
        }
    ))

    class Meta:
        model = Therapy_report
        fields = ['therapy_treatment',
                  'therapy_content',
                  'therapy_exercises',
                  'therapy_results',
                  'therapy'
                  ]
