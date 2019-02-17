from django import forms

class UploadFileForm(forms.Form):
    title = "Please upload a file: "
    file = forms.FileField()

class MultipleUploadFileForm(forms.Form):
	name = forms.CharField(max_length=50)
	water_use = forms.CharField(max_length=50, required=False)
	co2 = forms.CharField(max_length=50, required=False)
	land_use = forms.CharField(max_length=50, required=False)
	file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
