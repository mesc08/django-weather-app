from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import UserCreationForm
from django.forms import ModelForm, TextInput
from .models import City

class UserCreationForm(UserCreationForm):
	firstname = forms.CharField(max_length =30,  required = True)
	lastname = forms.CharField(max_length=30, required=True)
	email = forms.EmailField(max_length= 256, required=True, help_text='Required. Inform a valid email address')
	class Meta : 
		model =User
		fields = ('username', 'firstname', 'lastname', 'email', 'password1', 'password2')


class CityForm(ModelForm):
	class Meta:
		model = City
		fields =['name']
		widgets = {'name': TextInput(attrs ={'class':'input', 'placeholder' : 'City Name'})}