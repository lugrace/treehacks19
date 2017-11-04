from django import forms

class CollegeForm(forms.Form):
	your_college = forms.CharField(label='Enter a College', max_length=200)
	