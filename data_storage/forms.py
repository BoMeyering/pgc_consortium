"""
Data_Storage Forms
"""

from django import forms
from data_storage.models import GermplasmType, CommonName, Germplasm, Trial, Plot
from resources.models import Project


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

class TrialFilterForm(forms.Form):
    # projects = forms.ModelMultipleChoiceField(
    #     queryset=Project.objects.all(),
    #     widget=forms.SelectMultiple,
    #     required=False,
    #     label="Filter Projects"
    # )
    trials = forms.ModelMultipleChoiceField(
        queryset=Trial.objects.all(),
        widget=forms.SelectMultiple,
        required=True,
        label="Select field trials"
    )

class NewTrialForm(forms.ModelForm):
    class Meta:
        model = Trial
        fields = ['name', 'location_id', 'manager_id', 'project_id', 'affiliation_id', 'establishment_year', 'multi_year', 'experimental_unit_level']
        labels = {
            'name': 'Trial Name',
            'location_id': 'Location',
            'manager_id': 'Manager',
            'project_id': 'Project',
            'affiliation_id': 'Trial Affiliation',
            'establishment_year': 'Establishment Year',
            'multi_year': 'Multi-Year Trial?',
            'experimental_unit_level': 'Experimental Unit'
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the trial name'
            }),
            'location_id': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Where is this trial located?'
            }),
            'manager_id': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Who is the trial manager or contact?'
            }),
            'project_id': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Which project is this trial associated with?'
            }),
            'affiliation_id': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'What organization is the trial associated with?'
            }),
            'establishment_year': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'What year was this trial established?'
            }),
            'multi_year': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'experimental_unit_level': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select the smallest experimental unit level'
            }),

        }
