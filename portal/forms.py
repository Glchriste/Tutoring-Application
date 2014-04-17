from django import forms
from models import UploadFile

class AppointmentForm(forms.Form):
	email = forms.EmailField()
	course = forms.CharField(max_length=100)
	date = forms.CharField(max_length=100)
	comment = forms.CharField(widget=forms.Textarea)