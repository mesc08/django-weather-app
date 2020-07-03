from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from .forms import UserCreationForm, CityForm
from .models import City
from django.contrib.auth.decorators import login_required	
from django.db import IntegrityError
import requests
# Create your views here.
def home(request):
	return render(request, 'home.html')

def register(request):
	if request.method=='POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username=form.cleaned_data.get('username')
			raw_password=form.cleaned_data.get('password1')
			user = authenticate(username=username, password= raw_password)
			login(request,user)
			return redirect('main')
	else:
		form = UserCreationForm()
	return render(request,'register.html',{'form': form})

def login(request):
	if request.method=='GET':
		return render(request,'login.html',{'form':AuthenticationForm()})
	else:
		user = authenticate(request,username=request.POST['username'], password=request.POST['password'])
		if user is None:
			return render(request,'login.html',{'form':AuthenticationForm(),'error':'username and password did not match'})
		else:
			login(request,user)
			return redirect('mainpage')	
@login_required
def logout(request):
	if request.method=='POST':
		logout(request)
		return render(request, 'home.html')
@login_required
def mainpage(request):
	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=a961a2cacbe8a7fd5474db43e2455a3c'
	if request.method=='POST':
		form = CityForm(request.POST)
		form.save()
	form = CityForm()
	cities = City.objects.all()
	weather_data = []
	for city in cities:
		r = requests.get(url.format(city)).json()
		city_weather={
			'city': city.name,
			'temperature':r['main']['temp'],
			'description':r['weather'][0]['description'],
			'icon' : r['weather'][0]['icon'],
		}
		weather_data.append(city_weather)
	context = {'weather_data':weather_data, 'form': form}
	return render(request,'main.html', context)