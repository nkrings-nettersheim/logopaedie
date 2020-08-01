from django import forms
from django.forms import ModelForm

from .models import Parents_sheet


class ParentsSheetForm(ModelForm):
    class Meta:
        model: Parents_sheet
        fields = '__all__'
