import datetime
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Patient, Therapy, Process_report, Therapy_report, Doctor, Therapist, InitialAssessment, \
    Document, Document_therapy, Therapy_Something, Patient_Something, Diagnostic_group, Wait_list


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
            'placeholder': 'Geburtsdatum eingeben ...',
            'onchange': 'CheckDate(this.value, this.name)'
        }
    ),
        required=False
    )

    phone = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Format: 02251/11223344'
        }
    ),
        required=False
    )

    cell_phone = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Format: 0171/11223344'
        }
    ),
        required=False
    )

    active = forms.NullBooleanField(required=False, initial=True, widget=forms.CheckboxInput)

    inactive = forms.NullBooleanField(required=False, initial=False, widget=forms.CheckboxInput)


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


class SearchDiagnostic_groupForm(forms.Form):
    diagnostic_key = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'autofocus': 'autofocus',
            'placeholder': 'Kürzel eingeben ...'
        }
    ),
        required=False
    )


class DoctorForm(forms.ModelForm):
    doctor_name1 = forms.CharField(required=True,
                                   max_length=75,
                                   widget=forms.TextInput(
                                       attrs={
                                           'class': 'form-control',
                                           'autofocus': 'autofocus',
                                           'placeholder': 'Name eingeben ...'
                                       }
                                   )
                                   )

    doctor_name2 = forms.CharField(required=False,
                                   max_length=75,
                                   widget=forms.TextInput(
                                       attrs={
                                           'class': 'form-control',
                                           'placeholder': 'Weitere Namen eingeben ...'
                                       }
                                   )
                                   )

    doctor_name3 = forms.CharField(required=False,
                                   max_length=75,
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
                  'doctor_name3',
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

    tp_user_logopakt = forms.CharField(required=True,
                                       max_length=20,
                                       widget=forms.TextInput(
                                           attrs={
                                               'class': 'form-control',
                                               'placeholder': 'Nutzerkennung eingeben ...'
                                           }
                                       )
                                       )

    class Meta:
        model = Therapist
        fields = ['tp_first_name',
                  'tp_last_name',
                  'tp_initial',
                  'tp_user_logopakt'
                  ]


class Diagnostic_groupForm(forms.ModelForm):
    diagnostic_key = forms.CharField(required=True,
                                     max_length=10,
                                     widget=forms.TextInput(
                                         attrs={
                                             'class': 'form-control',
                                             'placeholder': 'Kürzel eingeben ...'
                                         }
                                     ))

    diagnostic_description = forms.CharField(required=True,
                                             max_length=250,
                                             widget=forms.TextInput(
                                                 attrs={
                                                     'class': 'form-control',
                                                     'placeholder': 'Diagnosegruppe eingeben ...'
                                                 }
                                             ))

    diagnostic_max_therapy = forms.IntegerField(required=True,
                                                widget=forms.NumberInput(
                                                )
                                                )

    class Meta:
        model = Diagnostic_group
        fields = [
            'diagnostic_key',
            'diagnostic_description',
            'diagnostic_max_therapy'
        ]


class PatientForm(forms.ModelForm):

    def clean_pa_phone(self):
        data = self.cleaned_data['pa_phone']
        if data:
            data = data.replace(' ', '')
            return data

    def clean_pa_cell_phone(self):
        data = self.cleaned_data['pa_cell_phone']
        if data:
            data = data.replace(' ', '')
            return data

    def clean_pa_cell_phone_add1(self):
        data = self.cleaned_data['pa_cell_phone_add1']
        if data:
            data = data.rsplit("/")
            rightdata = data[1].rsplit("(")
            data[0] = data[0].replace(' ', '')
            rightdata[0] = rightdata[0].replace(' ', '')
            data = data[0] + "/" + rightdata[0] + "  (" + rightdata[1]
            return data

    def clean_pa_cell_phone_add2(self):
        data = self.cleaned_data['pa_cell_phone_add2']
        if data:
            data = data.rsplit("/")
            rightdata = data[1].rsplit("(")
            data[0] = data[0].replace(' ', '')
            rightdata[0] = rightdata[0].replace(' ', '')
            data = data[0] + "/" + rightdata[0] + "  (" + rightdata[1]
            return data

    def clean_pa_date_of_birth(self):
        birthday = self.cleaned_data['pa_date_of_birth']
        if birthday > datetime.date.today():
            raise forms.ValidationError("Das Geburtsdatum darf nicht in der Zukunft liegen.")
        return birthday


    def clean(self):
        cleaned_data = super(PatientForm, self).clean()
        cell_phone_sms = cleaned_data['pa_cell_phone_sms']
        sms_yes_no = cleaned_data['pa_sms_no_yes']
        email = cleaned_data['pa_email']
        email_no_yes = cleaned_data['pa_email_no_yes']
        invoice_mail = cleaned_data['pa_invoice_mail']


        if cell_phone_sms == '' and sms_yes_no == False:
           self.add_error('pa_cell_phone_sms', forms.ValidationError("Bitte SMS Nummer erfassen."))

        if email == '' and email_no_yes == False:
           self.add_error('pa_email', forms.ValidationError("Bitte E-Mail erfassen."))

        if email == '' and invoice_mail == True:
           self.add_error('pa_invoice_mail', forms.ValidationError("Rechnung per E-Mail ohne E-Mail Adresse geht nicht ;-)"))

        return self.cleaned_data


    pa_first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Vornamen eingeben ...',
                'onchange': 'ucFirst(this.value, this.name)'
            }
        )
    )

    pa_last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'autofocus': 'autofocus',
                'placeholder': 'Nachnamen eingeben ...',
                'onchange': 'ucFirst(this.value, this.name)'
            }
        )
    )

    pa_street = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Strasse eingeben ...',
                'onchange': 'ucFirst(this.value, this.name)'
            }
        )
    )

    pa_city = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ort eingeben ...',
                'onchange': 'ucFirst(this.value, this.name)'
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
        max_length=60,
        widget=forms.TextInput(
            attrs={
                'pattern': '0[0-9\s]{2,5}/[0-9\s()A-Za-zÜÖÄüöäß]{0,60}',
                'class': 'form-control',
                'placeholder': 'Format: 0171/12233445 (Zusatzinfo)'
            }
        )
    )

    pa_cell_phone_add2 = forms.CharField(
        required=False,
        max_length=60,
        widget=forms.TextInput(
            attrs={
                'pattern': '0[0-9\s]{2,5}/[0-9\s()A-Za-zÜÖÄüöäß]{0,60}',
                'class': 'form-control',
                'placeholder': 'Format: 0171/12233445 (Zusatzinfo)'
            }
        )
    )

    pa_cell_phone_sms = forms.CharField(
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

    pa_email = forms.EmailField(
        required=False,
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'E-Mail Adresse erfassen'
            }
        )
    )

    #    pa_date_of_birth = forms.DateField(widget=AdminDateWidget())
    pa_date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={
                'pattern': '^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.]((19|20)\d\d)$',
                'class': 'form-control',
                'placeholder': 'Geburtsdatum Format: TT.MM.JJJJ',
                'onchange': 'CheckDate(this.value, this.name)'
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

    pa_allergy = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Allergie ? '
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

    pa_active_no_yes = forms.NullBooleanField(required=False, initial=True,
                                              widget=forms.CheckboxInput)

    pa_invoice_mail = forms.NullBooleanField(required=True,
                                                      error_messages={'blank': 'Bitte Ja oder Nein auswählen'},
                                                      widget=forms.NullBooleanSelect)


    pa_sms_no_yes = forms.NullBooleanField(required=False, initial=False,
                                              widget=forms.CheckboxInput)

    pa_email_no_yes = forms.NullBooleanField(required=False, initial=False,
                                              widget=forms.CheckboxInput)


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
                  'pa_cell_phone_sms',
                  'pa_email',
                  'pa_date_of_birth',
                  'pa_gender',
                  'pa_attention',
                  'pa_allergy',
                  'pa_note',
                  'pa_active_no_yes',
                  'pa_invoice_mail',
                  'pa_sms_no_yes',
                  'pa_email_no_yes'
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
        return data

    def clean_therapy_icd_cod(self):
        data = self.cleaned_data['therapy_icd_cod'].upper()
        data = data.replace(",", ".")
        return data

    def clean_therapy_icd_cod_2(self):
        data = self.cleaned_data['therapy_icd_cod_2'].upper()
        data = data.replace(",", ".")
        return data


    recipe_date = forms.DateField(required=True,
                                  widget=forms.DateInput(
                                      attrs={
                                          'class': 'form-control',
                                          'placeholder': 'Rezeptdatum eingeben ...',
                                          'onchange': 'CheckDate(this.value, this.name)'
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

    therapy_rid_of = forms.NullBooleanField(required=True,
                                            error_messages={'blank': 'Bitte Ja oder Nein auswählen'},
                                            widget=forms.NullBooleanSelect)

    therapy_report_no_yes = forms.NullBooleanField(required=True,
                                                   error_messages={'blank': 'Bitte Ja oder Nein auswählen'},
                                                   widget=forms.NullBooleanSelect)

    therapy_homevisit_no_yes = forms.NullBooleanField(required=True,
                                                      error_messages={'blank': 'Bitte Ja oder Nein auswählen'},
                                                      widget=forms.NullBooleanSelect)

    first_diagnostic_no_yes = forms.NullBooleanField(required=True,
                                                     error_messages={'blank': 'Bitte Ja oder Nein auswählen'},
                                                     widget=forms.NullBooleanSelect)

    need_diagnostic_no_yes = forms.NullBooleanField(required=True,
                                                    error_messages={'blank': 'Bitte Ja oder Nein auswählen'},
                                                    widget=forms.NullBooleanSelect)

    continue_diagnostic_no_yes = forms.NullBooleanField(required=True,
                                                    error_messages={'blank': 'Bitte Ja oder Nein auswählen'},
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
        ('SPZ', 'SPZ'),
        ('SCZ', 'SCZ'),
        ('OFZ', 'OFZ'),
    )

    therapy_indication_key = forms.ChoiceField(required=False, choices=INDICATION, label="", initial=1,
                                               widget=forms.Select(
                                                   attrs={
                                                       'class': 'form-control'
                                                   }
                                               ))

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

    therapy_icd_cod_2 = forms.CharField(required=True,
                                        max_length=10,
                                        error_messages={'blank': 'Bitte mind. ein - eingeben'},
                                        widget=forms.TextInput(
                                            attrs={
                                                'class': 'form-control',
                                                'placeholder': '2. ICD-CoD eingeben ...',
                                                'style': 'text-transform:uppercase;'
                                            }
                                        )
                                        )

    therapy_icd_cod_3 = forms.CharField(required=False,
                                        max_length=10,
                                        widget=forms.TextInput(
                                            attrs={
                                                'class': 'form-control',
                                                'placeholder': '3. ICD-CoD eingeben ...',
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

    diagnostic_group = forms.ModelChoiceField(queryset=Diagnostic_group.objects.all())

    class Meta:
        model = Therapy
        fields = ['id',
                  'recipe_date',
                  'therapy_regulation_amount',
                  'therapy_duration',
                  'therapy_frequence',
                  'therapy_rid_of',
                  'therapy_report_no_yes',
                  'therapy_homevisit_no_yes',
                  'therapy_indication_key',
                  'therapy_icd_cod',
                  'therapy_icd_cod_2',
                  'therapy_icd_cod_3',
                  'therapy_doctor',
                  'patients',
                  'therapists',
                  'diagnostic_group',
                  'first_diagnostic_no_yes',
                  'need_diagnostic_no_yes',
                  'continue_diagnostic_no_yes'
                  ]


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
                                        max_length=100,
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
                                          max_length=100,
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
                                          max_length=100,
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

    DURATION = (
        ('-', '-'),
        ('30', '30'),
        ('45', '45'),
        ('60', '60'),
    )

    therapy_start = forms.DateField(required=False,
                                    widget=forms.DateInput(
                                        attrs={
                                            'autofocus': 'autofocus',
                                            'class': 'form-control',
                                            'placeholder': 'Start der Therapie ...',
                                            'onchange': 'CheckDate(this.value, this.name)'
                                        }
                                    )
                                    )

    therapy_end = forms.DateField(required=False,
                                  widget=forms.DateInput(
                                      attrs={
                                          'class': 'form-control',
                                          'placeholder': 'Ende der Therapie ...',
                                          'onchange': 'CheckDate(this.value, this.name)'
                                      }
                                  )
                                  )

    report_date = forms.DateField(required=False,
                                  widget=forms.DateInput(
                                      attrs={
                                          'autofocus': 'autofocus',
                                          'class': 'form-control',
                                          'onchange': 'CheckDate(this.value, this.name)'
                                      }
                                  )
                                  )

    therapy_current_result = forms.CharField(required=False,
                                             max_length=820,
                                             widget=CKEditorWidget()
                                             )

    therapy_emphases = forms.CharField(required=False,
                                       max_length=820,
                                       widget=CKEditorWidget()
                                       )

    therapy_forecast = forms.CharField(required=False,
                                       max_length=820,
                                       widget=CKEditorWidget()
                                       )

    therapy_indicated = forms.NullBooleanField(required=False, widget=forms.CheckboxInput)

    #therapy_break = forms.NullBooleanField(required=False,
    #                                       widget=forms.CheckboxInput(
    #                                               attrs={
    #                                                   'onchange': "change_necessary_button();"
    #                                               }
    #                                           )
    #                                       )
    therapy_break = forms.NullBooleanField(required=False, widget=forms.CheckboxInput)

    therapy_break_internal = forms.NullBooleanField(required=False, widget=forms.CheckboxInput)

    #therapy_break_date = forms.DateField(required=False,
    #                                     widget=forms.DateInput(
    #                                         attrs={
    #                                             'class': 'form-control',
    #                                             'placeholder': 'Datum festlegen ...',
    #                                             'onchange': 'CheckDate(this.value, this.name)'
    #                                         }
    #                                     )
    #                                     )

    therapy_comment = forms.CharField(required=False,
                                      max_length=85,
                                      widget=forms.TextInput(
                                          attrs={
                                              'class': 'form-control',
                                              'placeholder': 'Bemerkung ...'
                                          }
                                      )
                                      )

    therapy_individual = forms.NullBooleanField(required=False, widget=forms.CheckboxInput)

    therapy_individual_min = forms.ChoiceField(choices=DURATION, label="", initial='-', widget=forms.Select(
        attrs={
            'class': 'form-control'
        }
    ))

    therapy_group = forms.NullBooleanField(required=False, widget=forms.CheckboxInput)

    therapy_group_min = forms.ChoiceField(choices=DURATION, label="", initial='-', widget=forms.Select(
        attrs={
            'class': 'form-control'
        }
    ))

    therapy_finish = forms.NullBooleanField(required=False, widget=forms.CheckboxInput)

    therapy_re_introduction = forms.NullBooleanField(required=False, widget=forms.CheckboxInput)

    therapy_re_introduction_weeks = forms.IntegerField(required=False,
                                                       initial=0,
                                                       widget=forms.NumberInput(
                                                       )
                                                       )

    therapy_frequence = forms.NullBooleanField(required=False, widget=forms.CheckboxInput)

    therapy_frequence_count_per_week = forms.CharField(required=False,
                                                       max_length=10,
                                                       widget=forms.TextInput(
                                                           attrs={
                                                               'class': 'form-control'
                                                           }
                                                       )
                                                       )

    therapy_another = forms.NullBooleanField(required=False, widget=forms.CheckboxInput)

    therapy_another_text = forms.CharField(required=False,
                                           max_length=20,
                                           widget=forms.TextInput(
                                               attrs={
                                                   'class': 'form-control'
                                               }
                                           )
                                           )

    therapy_home_visit = forms.NullBooleanField(required=False, widget=forms.CheckboxInput)

    therapy_necessary = forms.NullBooleanField(required=False,  widget=forms.CheckboxInput)


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
                  'therapy_break_internal',
                  #'therapy_break_date',
                  'therapy_comment',
                  'therapy',
                  'therapy_individual',
                  'therapy_individual_min',
                  'therapy_group',
                  'therapy_group_min',
                  'therapy_finish',
                  'therapy_re_introduction',
                  'therapy_re_introduction_weeks',
                  'therapy_frequence',
                  'therapy_frequence_count_per_week',
                  'therapy_another',
                  'therapy_another_text',
                  'therapy_home_visit',
                  'therapy_necessary']


class InitialAssessmentForm(forms.ModelForm):

    DIAGNOSTIC_LEVEL = (
        ('ED', 'Erst-Diagnostik'),
        ('BD', 'Bedarfs-Diagnostik'),
        ('WD', 'Weiterführende-Diagnostik')
    )

    ia_diagnostic_level = forms.ChoiceField(choices=DIAGNOSTIC_LEVEL,
                                            initial='ED',
                                            widget=forms.Select(
                                                attrs={
                                                    'class': 'form-control',
                                                    'autofocus': 'autofocus'
                                                }
                                            ))

    ia_date = forms.DateField(required=False,
                              widget=forms.DateInput(
                                  attrs={
                                      'class': 'form-control',
                                      'placeholder': 'Datum festlegen ...',
                                      'onchange': 'CheckDate(this.value, this.name)'
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

    ia_dysphagie = forms.CharField(required=False,
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
                                           'placeholder': 'Datum festlegen ...',
                                           'onchange': 'CheckDate(this.value, this.name)'
                                       }
                                   )
                                   )

    RESULT = (
        ('1', 'sehr gut'),
        ('2', 'gut'),
        ('3', 'befriedigend'),
        ('4', 'schlecht'),
        ('5', 'sehr schlecht'),
        ('6', 'nicht auswertbar')
    )

    ia_test_result = forms.ChoiceField(choices=RESULT, initial=6, widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ))

    ia_information = forms.CharField(required=False,
                                     max_length=300,
                                     widget=forms.Textarea(
                                         attrs={
                                             'class': 'form-control',
                                             'cols': '20',
                                             'rows': '5',
                                             'placeholder': "Notizen ..."
                                         }
                                     )
                                     )

    ia_first_diagnostic = forms.CharField(required=False, widget=CKEditorWidget(config_name='something'))


    class Meta:
        model = InitialAssessment
        fields = [
            'ia_date',
            'ia_assessment',
            'ia_artikulation',
            'ia_syntax',
            'ia_dysphagie',
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
            'ia_enhancement',
            'ia_information',
            'ia_first_diagnostic',
            'ia_diagnostic_level',
            'therapy'
        ]


class DocumentForm(forms.ModelForm):
    description = forms.CharField(required=True,
                                  max_length=100,
                                  widget=forms.TextInput(
                                      attrs={
                                          'class': 'form-control'
                                      }
                                  )
                                  )

    class Meta:
        model = Document
        fields = [
            'description',
            'document',
            'patient'
        ]


class DocumentTherapyForm(forms.ModelForm):
    description = forms.CharField(required=True,
                                  max_length=100,
                                  widget=forms.TextInput(
                                      attrs={
                                          'class': 'form-control'
                                      }
                                  )
                                  )

    class Meta:
        model = Document_therapy
        fields = [
            'description',
            'document',
            'therapy'
        ]


class TherapySomethingForm(forms.ModelForm):
    something_else = forms.CharField(widget=CKEditorWidget(config_name='something'))

    class Meta:
        model = Therapy_Something
        fields = [
            'something_else',
            'therapy'
        ]


class PatientSomethingForm(forms.ModelForm):
    pa_something_else = forms.CharField(widget=CKEditorWidget(config_name='something'))

    class Meta:
        model = Patient_Something
        fields = [
            'pa_something_else',
            'patient'
        ]


class WaitlistForm(forms.ModelForm):

    def clean_wl_phone(self):
        data = self.cleaned_data['wl_phone']
        if data:
            data = data.replace(' ', '')
            return data

    def clean_wl_cell_phone(self):
        data = self.cleaned_data['wl_cell_phone']
        if data:
            data = data.replace(' ', '')
            return data

    def clean_wl_cell_phone_add1(self):
        data = self.cleaned_data['wl_cell_phone_add1']
        if data:
            data = data.rsplit("/")
            rightdata = data[1].rsplit("(")
            data[0] = data[0].replace(' ', '')
            rightdata[0] = rightdata[0].replace(' ', '')
            data = data[0] + "/" + rightdata[0] + "  (" + rightdata[1]
            return data

    def clean_wl_cell_phone_add2(self):
        data = self.cleaned_data['wl_cell_phone_add2']
        if data:
            data = data.rsplit("/")
            rightdata = data[1].rsplit("(")
            data[0] = data[0].replace(' ', '')
            rightdata[0] = rightdata[0].replace(' ', '')
            data = data[0] + "/" + rightdata[0] + "  (" + rightdata[1]
            return data

    def clean(self):
        phone = self.cleaned_data['wl_phone']
        cell_phone = self.cleaned_data['wl_cell_phone']
        if phone == None and cell_phone == None:
            raise forms.ValidationError("Bitte Festnetz oder Mobilfunk erfassen!")


    wl_call_date = forms.DateField(
        required=True,
        initial=datetime.date.today,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Anrufddatum ...',
            }
        )
    )

    wl_active = forms.NullBooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput
    )

    wl_call_for = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Einbestellt ...',
            }
        )
    )

    wl_contact_person = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ansprechpartner ...',
            }
        )
    )
#    pa_something_else = forms.CharField(widget=CKEditorWidget(config_name='something'))
    wl_information = forms.CharField(required=False, widget=CKEditorWidget(config_name='default'))

    GENDER = (
        ('1', 'weiblich'),
        ('2', 'männlich'),
    )

    wl_gender = forms.ChoiceField(
        required=False,
        choices=GENDER,
        label="",
        initial=1,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
    ))

    wl_first_name = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Vornamen eingeben ...',
                'onchange': 'ucFirst(this.value, this.name)'
            }
        )
    )

    wl_last_name = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nachnamen eingeben ...',
                'autofocus': 'autofocus',
                'onchange': 'ucFirst(this.value, this.name)'
            }
        )
    )

    wl_street = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Strasse eingeben ...',
                'onchange': 'ucFirst(this.value, this.name)'
            }
        )
    )

    wl_city = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ort eingeben ...',
                'onchange': 'ucFirst(this.value, this.name)'
            }
        )
    )

    wl_date_of_birth = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Alter eingeben ...',
                'onchange': 'ucFirst(this.value, this.name)'
            }
        )
    )

    wl_phone = forms.CharField(
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

    wl_cell_phone = forms.CharField(
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

    wl_cell_phone_add1 = forms.CharField(
        required=False,
        max_length=60,
        widget=forms.TextInput(
            attrs={
                'pattern': '0[0-9\s]{2,5}/[0-9\s()A-Za-zÜÖÄüöäß]{0,60}',
                'class': 'form-control',
                'placeholder': 'Format: 0171/12233445 (Zusatzinfo)'
            }
        )
    )

    wl_cell_phone_add2 = forms.CharField(
        required=False,
        max_length=60,
        widget=forms.TextInput(
            attrs={
                'pattern': '0[0-9\s]{2,5}/[0-9\s()A-Za-zÜÖÄüöäß]{0,60}',
                'class': 'form-control',
                'placeholder': 'Format: 0171/12233445 (Zusatzinfo)'
            }
        )
    )

    wl_cell_phone_sms = forms.CharField(
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

    wl_email = forms.EmailField(
        required=False,
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'E-Mail Adresse erfassen'
            }
        )
    )

    wl_diagnostic = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Diagnose ...',
                'onchange': 'ucFirst(this.value, this.name)'
            }
        )
    )

    wl_appointment = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Termine? ...',
                'onchange': 'ucFirst(this.value, this.name)'
            }
        )
    )

    INSURANCE = (
        ('1', 'unbekannt'),
        ('2', 'gesetzlich'),
        ('3', 'privat'),
    )

    wl_insurance = forms.ChoiceField(
        required=False,
        choices=INSURANCE,
        label="",
        initial=1,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
    ))


    wl_recipe = forms.CharField(
        required=False,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Rezept? ...',
                'onchange': 'ucFirst(this.value, this.name)'
            }
        )
    )

    class Meta:
        model = Wait_list
        fields = [
            'wl_active',
            'wl_first_name',
            'wl_last_name',
            'wl_street',
            'wl_city',
            'wl_phone',
            'wl_cell_phone',
            'wl_cell_phone_add1',
            'wl_cell_phone_add2',
            'wl_cell_phone_sms',
            'wl_email',
            'wl_date_of_birth',
            'wl_gender',
            'wl_call_date',
            'wl_call_for',
            'wl_contact_person',
            'wl_information',
            'wl_diagnostic',
            'wl_appointment',
            'wl_insurance',
            'wl_recipe'
        ]