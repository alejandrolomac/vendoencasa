from django.urls import path, re_path, include
from django.contrib import admin
from . import views

app_name = "useradmin_app"

urlpatterns = [
	path('registrarse/', views.registerPage, name="registrarse"),
    path('entrar/', views.loginPage, name='entrar'),
    path('salir/', views.logoutUser, name='salir'),
    path('nueva-empresa/', views.registerCompany, name="registercompany"),
    path('entrar-miempresa/', views.loginPage, name='logincompany'),
] 