from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from .forms import UserCreationForm, CityForm
from .models import City
from django.contrib.auth.decorators import login_required	

# Create your views here.
def home(request):
	return render(request, 'home.html')

def register(request):
	if request.method == 'GET':
		

def login(request):


def logout(request):


def main(request):