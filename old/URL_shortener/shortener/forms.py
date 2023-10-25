from django import forms
from .validators import validate_url


class SubmitURLForm(forms.Form):
    url = forms.CharField(label="Your url to shorten", widget=forms.TextInput(
        attrs={'placeholder': 'URL to shorten'}), validators=[validate_url])
