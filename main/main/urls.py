from django.contrib import admin
from django.urls import path
from weather import views

urlpatterns = [
    path('admin/', admin.site.urls),

    #User Authentication
    path('registeruser/', views.registeruser, name="registeruser"),
    path('loginuser/',views.loginuser, name="loginuser"),
    path('logoutuser/',views.logoutuser, name="logoutuser"),

    #Use login main window
    path('', views.home, name = "home"),
    path('mainpage/',views.mainpage, name = "mainpage"),
    path('delete/<name>/', views.delete, name='delete'),
]
