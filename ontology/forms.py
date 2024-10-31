"""
data-storage forms
"""

from django import forms
from data_storage.models import TrialEvent


class TrialEventForm(forms.Form):
    class Meta:
        model = TrialEvent
        fields = ['process_id', 'trial_id', 'date' 'comment']

    name = forms.CharField()
    type = forms.ChoiceField(choices=GermplasmType)
    common_name = forms.ModelChoiceField(queryset=CommonName.objects.all(), empty_label='Select common name')
    genus = forms.CharField(max_length=255)
    species = forms.CharField(max_length=255)