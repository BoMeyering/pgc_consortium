"""
resource forms
"""

from django import forms
from .models import Project

class ContactForm(forms.Form):
    name = forms.CharField(max_length=255)
    your_email = forms.EmailField()
    subject = forms.CharField(max_length=255, required=True)
    message = forms.CharField(
        required=False,
        widget=forms.Textarea
    )

class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "funding", "website"]
        labels = {
            "name": "Project Name",
            "description": "Description", 
            "funding": "Funding",
            "website": "Website URL"
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the official or unofficial project name'
            }),
            'funding': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Funding agency, grant numbers, etc.'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'A url to the project website, if applicable'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Enter a short description of the main project goals'
            }),
        }