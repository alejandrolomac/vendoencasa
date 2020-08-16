from django.urls import path, re_path, include
from django.contrib import admin
from . import views

app_name = "useradmin_app"

urlpatterns = [
	path('registrarse/', views.registerDefault, name="registrarse"),
    path('entrar/', views.loginDefault, name='entrar'),
    path('entrar-usuario/', views.loginUsuarios, name='loginusuario'),
    path('salir/', views.logoutUser, name='salir'),
    path('nueva-empresa/', views.registerCompany, name="registercompany"),
    path('nuevo-usuario/', views.registerPage, name="registerusuario"),
    path('entrar-miempresa/', views.loginPage, name='logincompany'),
    path('perfil/', views.perfil, name='perfil'),
] 