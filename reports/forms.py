import datetime
from django import forms
# from django.contrib.admin.widgets import AdminDateWidget

from .models import Patient, Therapy, Process_report, Therapy_report, Doctor, Therapist, InitialAssessment
from .models import Document, Therapy_Something


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


class SearchTherapistForm(forms.Form):
    tp_initial = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'autofocus': 'autofocus',
            'placeholder': 'Kürzel eingeben ...'
        }
    ),
        required=False
    )


class SearchDoctorForm(forms.Form):
    name1 = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'autofocus': 'autofocus',
            'placeholder': 'Name eingeben ...'
        }
    ),
        required=False
    )

    lanr = forms.CharField(required=False, max_length=9, min_length=9,
                           widget=forms.TextInput(
                               attrs={
                                   'class': 'form-control',
                                   'autofocus': 'autofocus',
                                   'placeholder': 'Arztnummer eingeben (Zahnarzt mit "Z" starten) ...'
                               }
                           )
                           )


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

    doctor_lanr = forms.CharField(required=True,
                                  max_length=9,
                                  min_length=9,
                                  widget=forms.TextInput(
                                      attrs={
                                          'class': 'form-control',
                                          'placeholder': 'Arzt LANR eingeben ...'
                                      }
                                  )
                                  )

    class Meta:
        model = Doctor
        fields = ['doctor_name1',
                  'doctor_name2',
                  'doctor_street',
                  'doctor_zip_code',
                  'doctor_city',
                  'doctor_lanr'
                  ]


class TherapistForm(forms.ModelForm):
    tp_first_name = forms.CharField(required=True,
                                    max_length=50,
                                    widget=forms.TextInput(
                                        attrs={
                                            'class': 'form-control',
                                            'placeholder': 'Vorname eingeben ...'
                                        }
                                    )
                                    )

    tp_last_name = forms.CharField(required=False,
                                   max_length=50,
                                   widget=forms.TextInput(
                                       attrs={
                                           'class': 'form-control',
                                           'autofocus': 'autofocus',
                                           'placeholder': 'Name eingeben ...'
                                       }
                                   )
                                   )

    tp_initial = forms.CharField(required=True,
                                 max_length=5,
                                 widget=forms.TextInput(
                                     attrs={
                                         'class': 'form-control',
                                         'placeholder': 'Kürzel eingeben ...'
                                     }
                                 )
                                 )

    class Meta:
        model = Therapist
        fields = ['tp_first_name',
                  'tp_last_name',
                  'tp_initial'
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

    #    pa_date_of_birth = forms.DateField(widget=AdminDateWidget())
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

    def clean_therapy_doctor(self):
        data = self.cleaned_data['therapy_doctor']
        if len(data) == 9:
            therapy_doctor_instance = Doctor.objects.filter(doctor_lanr=data)
            if len(therapy_doctor_instance) == 1:
                therapy_doctor = Doctor.objects.get(doctor_lanr=data)
                return therapy_doctor
            else:
                raise forms.ValidationError("Arzt wurde nicht gefunden. Ggf. als neuen Arzt erfassen.")

    recipe_date = forms.DateField(required=True,
                                  widget=forms.DateInput(
                                      attrs={
                                          'class': 'form-control',
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

    # therapy_doctor = forms.ModelChoiceField(queryset=Doctor.objects.order_by('doctor_lanr'))

    therapy_doctor = forms.CharField(required=True, max_length=9, min_length=9,
                                     widget=forms.TextInput(
                                         attrs={
                                             'class': 'form-control',
                                             'placeholder': '9-stellige Arztnummer ...'
                                         }
                                     ))

    patients = forms.ModelChoiceField(queryset=Patient.objects.all())

    therapists = forms.ModelChoiceField(queryset=Therapist.objects.all())

    class Meta:
        model = Therapy
        fields = ['id',
                  'recipe_date',
                  'therapy_regulation_amount',
                  'therapy_duration',
                  'therapy_frequence',
                  'therapy_rid_of',
                  'therapy_report_no_yes',
                  'therapy_indication_key',
                  'therapy_icd_cod',
                  'therapy_doctor',
                  'patients',
                  'therapists']


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


class InitialAssessmentForm(forms.ModelForm):
    ia_date = forms.DateField(required=False,
                              widget=forms.DateInput(
                                  attrs={
                                      'class': 'form-control',
                                      'autofocus': 'autofocus',
                                      'placeholder': 'Datum festlegen ...'
                                  }
                              )
                              )

    ia_assessment = forms.CharField(required=False,
                                    max_length=100,
                                    widget=forms.TextInput(
                                        attrs={
                                            'class': 'form-control'
                                        }
                                    )
                                    )

    ia_artikulation = forms.CharField(required=False,
                                      max_length=100,
                                      widget=forms.TextInput(
                                          attrs={
                                              'class': 'form-control'
                                          }
                                      )
                                      )

    ia_syntax = forms.CharField(required=False,
                                max_length=100,
                                widget=forms.TextInput(
                                    attrs={
                                        'class': 'form-control'
                                    }
                                )
                                )

    ia_semantik = forms.CharField(required=False,
                                  max_length=100,
                                  widget=forms.TextInput(
                                      attrs={
                                          'class': 'form-control'
                                      }
                                  )
                                  )

    ia_understanding = forms.CharField(required=False,
                                       max_length=100,
                                       widget=forms.TextInput(
                                           attrs={
                                               'class': 'form-control'
                                           }
                                       )
                                       )

    ia_expiration = forms.CharField(required=False,
                                    max_length=100,
                                    widget=forms.TextInput(
                                        attrs={
                                            'class': 'form-control'
                                        }
                                    )
                                    )

    ia_motor_skills = forms.CharField(required=False,
                                      max_length=100,
                                      widget=forms.TextInput(
                                          attrs={
                                              'class': 'form-control'
                                          }
                                      )
                                      )

    ia_perception = forms.CharField(required=False,
                                    max_length=100,
                                    widget=forms.TextInput(
                                        attrs={
                                            'class': 'form-control'
                                        }
                                    )
                                    )

    ia_breathing = forms.CharField(required=False,
                                   max_length=100,
                                   widget=forms.TextInput(
                                       attrs={
                                           'class': 'form-control'
                                       }
                                   )
                                   )

    ia_other = forms.CharField(required=False,
                               max_length=100,
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control'
                                   }
                               )
                               )

    ia_test = forms.CharField(required=False,
                              max_length=100,
                              widget=forms.TextInput(
                                  attrs={
                                      'class': 'form-control'
                                  }
                              )
                              )

    ia_test_date = forms.DateField(required=False,
                                   widget=forms.DateInput(
                                       attrs={
                                           'class': 'form-control',
                                           'placeholder': 'Datum festlegen ...'
                                       }
                                   )
                                   )

    class Meta:
        model = InitialAssessment
        fields = [
            'ia_date',
            'ia_assessment',
            'ia_artikulation',
            'ia_syntax',
            'ia_semantik',
            'ia_understanding',
            'ia_expiration',
            'ia_motor_skills',
            'ia_perception',
            'ia_breathing',
            'ia_other',
            'ia_test',
            'ia_test_date',
            'ia_test_result',
            'therapy'
        ]


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = [
            'description',
            'document',
            'patient'
        ]


class TherapySomethingForm(forms.ModelForm):
    something_else = forms.CharField(required=False,
                                     widget=forms.Textarea(
                                         attrs={
                                             'class': 'form-control',
                                             'cols': '50',
                                             'rows': '20'
                                         }
                                     ))

    class Meta:
        model = Therapy_Something
        fields = [
            'something_else',
            'therapy'
        ]
