from django import forms
from .models import UploadModel
from django.forms import ClearableFileInput

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadModel
        fields = ['files']
        widgets = {
            "files": ClearableFileInput(attrs={'multiple': True}),
        }
        labels = {
            "files": ""
       }

