import datetime
from django import forms
from reportlab.platypus.paragraph import strip

from .models import Patient, Therapy, Process_report, Therapy_report, Doctor


class IndexForm(forms.Form):
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'autofocus': 'autofocus',
            'placeholder': 'Name eingeben ...'
        }
    ),
        required=False
    )

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Vornamen eingeben ...'
        }
    ),
        required=False
    )

    date_of_birth = forms.DateField(widget=forms.DateInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Geburtsdatum eingeben ...'
        }
    ),
        required=False
    )


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
                                   max_length=50,
                                   widget=forms.TextInput(
                                       attrs={
                                           'class': 'form-control',
                                           'autofocus': 'autofocus',
                                           'placeholder': 'Name eingeben ...'
                                       }
                                   )
                                   )

    doctor_name2 = forms.CharField(required=False,
                                   max_length=50,
                                   widget=forms.TextInput(
                                       attrs={
                                           'class': 'form-control',
                                           'placeholder': 'Weitere Namen eingeben ...'
                                       }
                                   )
                                   )

    doctor_street = forms.CharField(required=True,
                                    max_length=50,
                                    widget=forms.TextInput(
                                        attrs={
                                            'class': 'form-control',
                                            'placeholder': 'Strasse eingeben ...'
                                        }
                                    )
                                    )

    doctor_zip_code = forms.CharField(required=True,
                                      max_length=5,
                                      widget=forms.TextInput(
                                          attrs={
                                              'class': 'form-control',
                                              'placeholder': 'PLZ eingeben ...'
                                          }
                                      )
                                      )

    doctor_city = forms.CharField(required=True,
                                  max_length=50,
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

    def clean_pa_phone(self):

        charvalue = ''
        charvalue2 = ''
        data = self.cleaned_data['pa_phone']
        if data:
            data = data.replace(' ', '')
            data = data.rsplit("/")
            if len(data[1]) % 2:
                for char in data[1]:
                    charvalue = charvalue + char
                    charvalue2 = charvalue2 + char
                    if len(charvalue2) % 2:
                        charvalue = charvalue + " "
            else:
                for char in data[1]:
                    charvalue = charvalue + char
                    charvalue2 = charvalue2 + char
                    if not len(charvalue2) % 2:
                        charvalue = charvalue + " "

            data = data[0] + " / " + charvalue
            return data

    def clean_pa_cell_phone(self):
        charvalue = ''
        charvalue2 = ''
        data = self.cleaned_data['pa_cell_phone']
        if data:
            data = data.replace(' ', '')
            data = data.rsplit("/")
            if len(data[1]) % 2:
                for char in data[1]:
                    charvalue = charvalue + char
                    charvalue2 = charvalue2 + char
                    if len(charvalue2) % 2:
                        charvalue = charvalue + " "
            else:
                for char in data[1]:
                    charvalue = charvalue + char
                    charvalue2 = charvalue2 + char
                    if not len(charvalue2) % 2:
                        charvalue = charvalue + " "

            data = data[0] + " / " + charvalue
            return data

    def clean_pa_cell_phone_add1(self):
        charvalue = ''
        charvalue2 = ''
        data = self.cleaned_data['pa_cell_phone_add1']
        if data:
            data = data.replace(' ', '')
            data = data.rsplit("/")
            rightdata = data[1].rsplit("(")

            if len(rightdata[0]) % 2:
                for char in rightdata[0]:
                    charvalue = charvalue + char
                    charvalue2 = charvalue2 + char
                    if len(charvalue2) % 2:
                        charvalue = charvalue + " "
            else:
                for char in rightdata[0]:
                    charvalue = charvalue + char
                    charvalue2 = charvalue2 + char
                    if not len(charvalue2) % 2:
                        charvalue = charvalue + " "

            data = data[0] + " / " + charvalue + "  (" + rightdata[1]
            return data

    def clean_pa_cell_phone_add2(self):
        charvalue = ''
        charvalue2 = ''
        data = self.cleaned_data['pa_cell_phone_add2']
        if data:
            data = data.replace(' ', '')
            data = data.rsplit("/")
            rightdata = data[1].rsplit("(")

            if len(rightdata[0]) % 2:
                for char in rightdata[0]:
                    charvalue = charvalue + char
                    charvalue2 = charvalue2 + char
                    if len(charvalue2) % 2:
                        charvalue = charvalue + " "
            else:
                for char in rightdata[0]:
                    charvalue = charvalue + char
                    charvalue2 = charvalue2 + char
                    if not len(charvalue2) % 2:
                        charvalue = charvalue + " "

            data = data[0] + " / " + charvalue + "  (" + rightdata[1]
            return data

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

    pa_phone = forms.CharField(
        required=False,
        max_length=35,
        widget=forms.TextInput(
            attrs={
                'pattern': '0[0-9\s]{2,5}/[0-9\s]{0,20}',
                'class': 'form-control',
                'placeholder': 'Format: 02251/11223344'
            }
        )
    )

    pa_cell_phone = forms.CharField(
        required=False,
        max_length=35,
        widget=forms.TextInput(
            attrs={
                'pattern': '0[0-9\s]{2,5}/[0-9\s]{0,20}',
                'class': 'form-control',
                'placeholder': 'Format: 0171/12233445'
            }
        )
    )

    pa_cell_phone_add1 = forms.CharField(
        required=False,
        max_length=35,
        widget=forms.TextInput(
            attrs={
                'pattern': '0[0-9\s]{2,5}/[0-9\s()A-Za-zÜÖÄüöäß]{0,30}',
                'class': 'form-control',
                'placeholder': 'Format: 0171/12233445 (Zusatzinfo)'
            }
        )
    )

    pa_cell_phone_add2 = forms.CharField(
        required=False,
        max_length=35,
        widget=forms.TextInput(
            attrs={
                'pattern': '0[0-9\s]{2,5}/[0-9\s()A-Za-zÜÖÄüöäß]{0,30}',
                'class': 'form-control',
                'placeholder': 'Format: 0171/12233445 (Zusatzinfo)'
            }
        )
    )

    pa_date_of_birth = forms.DateField(
        required=True,
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

    pa_attention = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Wichtige Info ...'
            }
        )
    )

    pa_note = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'cols': '20',
                'rows': '5',
                'placeholder': "Notizen ..."
            }
        )
    )

    class Meta:
        model = Patient
        fields = ['pa_first_name',
                  'pa_last_name',
                  'pa_street',
                  'pa_city',
                  'pa_phone',
                  'pa_cell_phone',
                  'pa_cell_phone_add1',
                  'pa_cell_phone_add2',
                  'pa_date_of_birth',
                  'pa_gender',
                  'pa_attention',
                  'pa_note'
                  ]


class TherapyForm(forms.ModelForm):

    def check_indication(value):
        if value == "n/a":
            raise forms.ValidationError("Bitte Indikationsschlüssel auswählen")

    recipe_date = forms.DateField(required=True,
                                  widget=forms.DateInput(
                                      attrs={
                                          'class': 'form-control',
                                          'autofocus': 'autofocus',
                                          'placeholder': 'Rezeptdatum eingeben ...'
                                      }
                                  )
                                  )


    therapy_regulation_amount = forms.IntegerField(required=True,
                                                   widget=forms.NumberInput(
                                                   )
                                                   )

    therapy_frequence = forms.CharField(required=True,
                                        max_length=5,
                                        widget=forms.TextInput(
                                            attrs={
                                                'class': 'form-control',
                                                'placeholder': 'Therapiefrequenz erfassen ...'
                                            }
                                        )
                                        )

    DURATION = (
        ('30', '30'),
        ('45', '45'),
        ('60', '60'),
    )

    therapy_duration = forms.ChoiceField(choices=DURATION, label="", initial=45, widget=forms.Select(
        attrs={
            'class': 'form-control'
        }
    ))
    therapy_rid_of = forms.NullBooleanField(required=False, initial=False, widget=forms.NullBooleanSelect)

    therapy_report_no_yes = forms.NullBooleanField(required=True,
                                                   widget=forms.NullBooleanSelect)

    INDICATION = (
        ('n/a', 'auswählen'),
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
    ), validators=[check_indication, ])

    therapy_icd_cod = forms.CharField(required=True,
                                      max_length=10,
                                      widget=forms.TextInput(
                                          attrs={
                                              'class': 'form-control',
                                              'placeholder': 'ICD-CoD eingeben ...',
                                              'style': 'text-transform:uppercase;'
                                          }
                                      )
                                      )

    therapy_doctor = forms.ModelChoiceField(queryset=Doctor.objects.all())

    patients = forms.ModelChoiceField(queryset=Patient.objects.all())

    class Meta:
        model = Therapy
        fields = ['recipe_date',
                  'therapy_regulation_amount',
                  'therapy_duration',
                  'therapy_frequence',
                  'therapy_rid_of',
                  'therapy_report_no_yes',
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

    process_content = forms.CharField(required=True,
                                      widget=forms.Textarea(
                                          attrs={
                                              'class': 'form-control',
                                              'autofocus': 'autofocus',
                                              'cols': '20',
                                              'rows': '5'
                                          }
                                      )
                                      )

    process_exercises = forms.CharField(required=False,
                                        max_length=10,
                                        widget=forms.TextInput(
                                            attrs={
                                                'class': 'form-control'
                                            }
                                        )
                                        )

    process_results = forms.CharField(required=False,
                                      max_length=20,
                                      widget=forms.TextInput(
                                          attrs={
                                              'class': 'form-control'
                                          }
                                      )
                                      )

    process_content_2 = forms.CharField(required=False,
                                        widget=forms.Textarea(
                                            attrs={
                                                'class': 'form-control',
                                                'cols': '20',
                                                'rows': '5'
                                            }
                                        )
                                        )

    process_exercises_2 = forms.CharField(required=False,
                                          max_length=20,
                                          widget=forms.TextInput(
                                              attrs={
                                                  'class': 'form-control'
                                              }
                                          )
                                          )

    process_results_2 = forms.CharField(required=False,
                                        max_length=20,
                                        widget=forms.TextInput(
                                            attrs={
                                                'class': 'form-control'
                                            }
                                        )
                                        )

    process_content_3 = forms.CharField(required=False,
                                        widget=forms.Textarea(
                                            attrs={
                                                'class': 'form-control',
                                                'cols': '20',
                                                'rows': '5'
                                            }
                                        )
                                        )

    process_exercises_3 = forms.CharField(required=False,
                                          max_length=20,
                                          widget=forms.TextInput(
                                              attrs={
                                                  'class': 'form-control'
                                              }
                                          )
                                          )

    process_results_3 = forms.CharField(required=False,
                                        max_length=20,
                                        widget=forms.TextInput(
                                            attrs={
                                                'class': 'form-control'
                                            }
                                        )
                                        )

    class Meta:
        model = Process_report
        fields = ['process_treatment',
                  'process_content',
                  'process_exercises',
                  'process_results',
                  'process_content_2',
                  'process_exercises_2',
                  'process_results_2',
                  'process_content_3',
                  'process_exercises_3',
                  'process_results_3',
                  'therapy'
                  ]


class TherapyReportForm(forms.ModelForm):
    now = datetime.datetime.now()
    placeholder = now.strftime('%d.%m.%Y')

    therapy_start = forms.DateField(required=False,
                                    widget=forms.DateInput(
                                        attrs={
                                            'autofocus': 'autofocus',
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

    report_date = forms.DateField(required=False,
                                  widget=forms.DateInput(
                                      attrs={
                                          'autofocus': 'autofocus',
                                          'class': 'form-control'
                                      }
                                  )
                                  )

    therapy_current_result = forms.CharField(required=False,
                                             max_length=700,
                                             widget=forms.Textarea(
                                                 attrs={
                                                     'class': 'form-control',
                                                     'cols': '50',
                                                     'rows': '6'
                                                 }
                                             ))

    therapy_emphases = forms.CharField(required=False,
                                       max_length=700,
                                       widget=forms.Textarea(
                                           attrs={
                                               'class': 'form-control',
                                               'cols': '50',
                                               'rows': '6'
                                           }
                                       ))

    therapy_forecast = forms.CharField(required=False,
                                       max_length=700,
                                       widget=forms.Textarea(
                                           attrs={
                                               'class': 'form-control',
                                               'cols': '50',
                                               'rows': '6'
                                           }
                                       ))

    therapy_indicated = forms.NullBooleanField(required=False, widget=forms.CheckboxInput)

    therapy_break = forms.NullBooleanField(required=False, widget=forms.CheckboxInput)

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
        fields = ['therapy_start',
                  'therapy_end',
                  'report_date',
                  'therapy_current_result',
                  'therapy_emphases',
                  'therapy_forecast',
                  'therapy_indicated',
                  'therapy_break',
                  'therapy_break_date',
                  'therapy_comment',
                  'therapy']
