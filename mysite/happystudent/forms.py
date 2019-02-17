from django import forms
import base64
import re
# from crispy_forms.helper import FormHelper

class CollegeForm(forms.Form):
	your_college = forms.CharField(label='Enter a College')
	
class UploadFileForm(forms.Form):
    title = "Please upload a file: "#forms.CharField(max_length=50)
    file = forms.FileField()

class UploadFileScreenshotForm(forms.Form):
    # title = "Please upload a file: "#forms.CharField(max_length=50)
    file = forms.FileField()
    
class MultipleUploadFileForm(forms.Form):
	name = forms.CharField(max_length=50)
	water_use = forms.CharField(max_length=50, required=False)
	co2 = forms.CharField(max_length=50, required=False)
	land_use = forms.CharField(max_length=50, required=False)
	upload_files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
