from django import forms
from .models import UploadModel
from django.core.files.storage import FileSystemStorage
from django.forms import ClearableFileInput
from django.conf import settings
import os


class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

class UploadFileForm(forms.ModelForm):
    files = forms.FileField(upload_to="CSVFiles/",  storage=OverwriteStorage())

    class Meta:
        model = UploadModel
        fields = ['files']
        widgets = {
            "files": ClearableFileInput(attrs={'multiple': True}),
        }

