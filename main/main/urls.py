from django.contrib import admin
from django.urls import path
from weather import views

urlpatterns = [
    path('admin/', admin.site.urls),

    #User Authentication
    path('register/', views.register, name="register"),
    path('login/',views.login, name="login"),
    path('logout/',views.logout, name="logout"),

    #Use login main window
    path('home/', views.home, name = "home"),
    path('main/',views.main, name = "main"),
]
