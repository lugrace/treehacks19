from django import forms

class UploadFileForm(forms.Form):
    title = "Please upload a file: "
    file = forms.FileField()

class MultipleUploadFileForm(forms.Form):
	title = forms.CharField(max_length=50)
	file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
