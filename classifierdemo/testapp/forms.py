from django import forms

class UploadFileForm(forms.Form):
    title = "Please upload a file: "#forms.CharField(max_length=50)
    file = forms.FileField()