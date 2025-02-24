
from django import forms

from .models import Parents_sheet


class ParentsSheetForm(forms.ModelForm):

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
            'email'
        ]
