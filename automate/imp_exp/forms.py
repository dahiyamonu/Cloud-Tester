from django import forms

class UploadFileForm(forms.Form):
    """Form for uploading a file."""
    file = forms.FileField(label="Upload File")
