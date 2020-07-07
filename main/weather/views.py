from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from .forms import UserForm, CityForm
from .models import City, Info
from django.contrib.auth.decorators import login_required	
from django.db import IntegrityError
import requests

def home(request):
	return render(request, 'home.html')

def registeruser(request):
	if request.method == 'POST':
		uname = request.POST['username']
		em  = request.POST['email']
		pass1 = request.POST['password1']
		pass2 = request.POST['password2']
		form = UserForm()
		if pass1 == pass2:
			if User.objects.filter(username =uname).exists():
				return render(request,'register.html',{'form':form,'error':'Username already taken'})
			else:
				if User.objects.filter(email=em).exists():
					return render(request,'register.html',{'form':form,'error':'Email-id already taken'})
				else:
					user = User.objects.create_user(username=uname,email = em, password=pass1)
					user.save()
					return redirect('loginuser')
		else:
			return render(request,"register.html",{'form':form,'error':'Password not matching'})
	else:
		form = UserForm()
		return render(request,'register.html',{'form':form})
        
def loginuser(request):
	if request.method=='GET':
		return render(request,'login.html',{'form':AuthenticationForm()})
	else:
		user = authenticate(request,username=request.POST['username'], password=request.POST['password'])
		if user is None:
			return render(request,'login.html',{'form':AuthenticationForm(),'error':'username and password did not match'})
		else:
			login(request, user)
			return redirect('mainpage')	

@login_required
def logoutuser(request):
		logout(request)
		return redirect('home')
@login_required
def mainpage(request):
    flag = False
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=2a5035a1a9287c44491f251ad0719454'
    cities = City.objects.all()
    weather_data = []
    ex_weather_data = []
    form = CityForm()
    message = ''
    if request.method == 'POST':
        if 'city' in request.POST:
            form = CityForm(request.POST)
            if form.is_valid():
                temp = form.cleaned_data['name'].capitalize()
                x = City.objects.filter(name=temp).count()
                cod = requests.get(url.format(temp)).json()['cod']
                if x == 0 and cod != '404':
                    c = City(name=temp)
                    c.save()
                    request.user.city.add(c)
                elif x != 0:
                    for c in request.user.city.all():
                        if temp == c.name:
                            message = 'City already loaded.'
                            flag = True
                    if not flag:
                        c = City(name=temp)
                        c.save()
                        request.user.city.add(c)
                elif cod == '400':
                    message = 'Invalid city.'
    if request.user.is_authenticated:
        for city in cities:
            if city in request.user.city.all():
                city_weather = requests.get(url.format(city)).json()
                weather = {
                    'city': str(city).capitalize(),
                    'temperature': city_weather['main']['temp'],
                    'description': city_weather['weather'][0]['description'],
                    'icon': city_weather['weather'][0]['icon']
                }
                weather_data.append(weather)
                ex_weather = {
                    'city': str(city).capitalize(),
                    'temperature': city_weather['main']['temp'],
                    'feels_like': city_weather['main']['feels_like'],
                    'pressure': city_weather['main']['pressure'],
                    'humidity': city_weather['main']['humidity'],
                    'description': city_weather['weather'][0]['description'],
                    'icon': city_weather['weather'][0]['icon'],
                    'wind_speed': city_weather['wind']['speed']
                }
                ex_weather_data.append(ex_weather)
    context = {
        'weather_data': weather_data,
        'ex_weather_data': ex_weather_data,
        'form': form,
        'messages': message,
    }
    return render(request, 'main.html', context)
@login_required
def delete(request, name):
    request.user.city.all().filter(name=name).delete()
    return redirect('mainpage')