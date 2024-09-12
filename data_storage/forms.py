"""
Data_Storage Forms
"""

from django import forms
from .models import GermplasmType, CommonName, Germplasm

class GermplasmForm(forms.Form):
    class Meta:
        model = Germplasm
        fields = ['name', 'type', 'common_name', 'genus', 'species']

    name = forms.CharField(max_length=255)
    type = forms.ChoiceField(choices=GermplasmType)
    common_name = forms.ModelChoiceField(queryset=CommonName.objects.all(), empty_label='Select common name')
    genus = forms.CharField(max_length=255)
    species = forms.CharField(max_length=255)

class EmailContactForm(forms.Form):
    name = forms.CharField(max_length=255)
    your_email = forms.EmailField()
    subject = forms.CharField(max_length=255, required=True)
    message = forms.CharField(
        required=False,
        widget=forms.Textarea
    )