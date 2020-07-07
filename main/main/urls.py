from django.contrib import admin
from django.urls import path
from weather import views

urlpatterns = [
    path('admin/', admin.site.urls),

    #User Authentication
    path('register/', views.register, name="register"),
    path('login/',views.loginuser, name="login"),
    path('logout/',views.logoutuser, name="logout"),

    #Use login main window
    path('', views.home, name = "home"),
    path('mainpage/',views.mainpage, name = "mainpage"),
]
