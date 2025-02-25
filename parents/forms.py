
from django import forms

from .models import Parents_sheet


class ParentsSheetFormStep1(forms.ModelForm):

    child_last_name = forms.CharField(
        label="Name*",
        max_length=75,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Name des Kindes",
                "style": "width: 300px;"
            })
    )

    child_first_name = forms.CharField(
        required=True,
        label="Vorname*",
        max_length=75,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Vorname des Kindes",
                "style": "width: 300px;"
            })
    )

    child_day_of_birth = forms.CharField(
        required=True,
        label="geb.*",
        max_length=25,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Geburtstag",
                "style": "width: 200px;"
            })
    )

    health_assurance = forms.CharField(
        required=False,
        label="Krankenversicherung",
        max_length=75,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Krankenkasse",
                "style": "width: 300px;"
            })
    )

    doctor = forms.CharField(
        required=False,
        label="überweisender Arzt",
        max_length=75,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "überweisender Arzt",
                "style": "width: 300px;"
            })
    )

    phone = forms.CharField(
        required=False,
        label="Telefon",
        max_length=75,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Format 02251/Rufnummer",
                "style": "width: 300px;"
            })
    )

    cellphone = forms.CharField(
        required=False,
        label="Mobil",
        max_length=75,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Format 01xy/Rufnummer",
                "style": "width: 300px;"
            })
    )

    phone_work = forms.CharField(
        required=False,
        label="Dienstlich",
        max_length=75,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Format Vorwahl/Rufnummer",
                "style": "width: 300px;"
            })
    )

    email = forms.CharField(
        required=False,
        label="eMail",
        max_length=75,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "eMail Adresse",
                "style": "width: 500px;"
            })
    )

    class Meta:
        model = Parents_sheet
        fields = [
            'child_last_name',
            'child_first_name',
            'child_day_of_birth',
            'health_assurance',
            'doctor',
            'phone',
            'cellphone',
            'phone_work',
            'email',
            'mother_last_name',
            'mother_first_name',
            'mother_day_of_birth',
            'mother_job',
            'father_last_name',
            'father_first_name',
            'father_day_of_birth',
            'father_job',
            'siblings1_last_name',
            'siblings1_first_name',
            'siblings1_age',
            'siblings2_last_name',
            'siblings2_first_name',
            'siblings2_age',
            'siblings3_last_name',
            'siblings3_first_name',
            'siblings3_age'
        ]

class ParentsSheetFormStep2(forms.ModelForm):

    class Meta:
        model = Parents_sheet
        fields = [
            'problems_pregnancy',
            'problems_pregnancy_yes',
            'problems_family_speak_listen',
            'problems_family_speak_listen_yes',
            'child_allergy',
            'child_allergy_yes',
            'crawl_age',
            'crawl_age_advise',
            'walk_age',
            'walk_age_advise',
            'child_dev_1',
            'child_dev_2',
            'child_dev_3',
            'child_dev_4',
            'child_dev_language',
            'child_dev_language_yes',
            'child_dev_5',
            'child_left_handed'
        ]


class ParentsSheetFormStep3(forms.ModelForm):
    class Meta:
        model = Parents_sheet
        fields = [
            'child_chronic_disease',
            'child_chronic_disease_yes',
            'child_nutrition',
            'child_hospital_visits',
            'child_hospital_visits_yes',
            'child_medicine',
            'child_medicine_yes',
            'child_count_colds',
            'child_timpani_tube',
            'child_listen',
            'child_illness_1',
            'child_illness_2',
            'child_what_teething'
        ]


class ParentsSheetFormStep4(forms.ModelForm):
    class Meta:
        model = Parents_sheet
        fields = [
            'child_glases',
            'child_hearing_aid',
            'child_problems_sleeping_hearing',
            'child_problems_sleeping_hearing_yes',
            'child_use_of_language',
            'child_speaking_interrupt',
            'child_speaking_interrupt_yes',
            'child_speaking_dev',
            'child_speaking_dev_yes',
            'child_mimik',
            'child_understanding',
            'child_letter_wrong',
            'child_letter_wrong_yes',
            'child_sentence_construction',
            'child_speech',
            'child_noises_reaktion',
            'child_watch_contact',
            'child_talking',
            'child_stutter'
        ]


class ParentsSheetFormStep5(forms.ModelForm):
    class Meta:
        model = Parents_sheet
        fields = [
            'child_development',
            'child_playing_1',
            'child_playing_2',
            'child_playing_3',
            'child_school',
            'child_school_yes',
            'child_school_which'
        ]


class ParentsSheetFormStep6(forms.ModelForm):
    class Meta:
        model = Parents_sheet
        fields = [
            'child_caregivers',
            'child_speech_therapy',
            'child_speech_therapy_yes',
            'child_speech_therapy_advise'
        ]
