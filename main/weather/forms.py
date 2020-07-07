from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput
from .models import City

class UserForm(UserCreationForm):
	email = forms.EmailField(max_length= 256, required=True)
	class Meta : 
		model =User
		fields = ('username', 'email', 'password1', 'password2',)

class CityForm(ModelForm):
	class Meta:
		model = City
		fields =['name']
		widgets = {'name': TextInput(attrs ={'class':'input', 'placeholder' : 'City Name'})}