"""
resource forms
"""

from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=255)
    your_email = forms.EmailField()
    subject = forms.CharField(max_length=255, required=True)
    message = forms.CharField(
        required=False,
        widget=forms.Textarea
    )