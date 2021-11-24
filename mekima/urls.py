"""mekima URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from mekima.views import  *
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index),
    path('perfil/', perfil),
    path('iniciarCuenta/', iniciarCuenta),
    path('iniciarSesion/', iniciarSesion),
    path('crearCuenta/', crearCuenta),
    path('crearCuentaN/', crearCuentaN),
    path('NSelector/', NSelector),
    path('WSelector/', WSelector),
    path('jugar/', JUGaR),
    path('normal/', normal),
    path('words/', words),
    path('registrarpuntajeN/<puntaje>', registrarPN),
    path('registrarpuntajeW/<puntaje>', registrarPW),
    path('modificarCuenta/', modificarDatos),
    path('modificarDatos/', modificarCuenta),
    path('cerrarSesion/', CerrarSesion),
    path('historial/', Historial),
    path('normal-cam/',configurar ),
    path('jugarNormal/',jugarNormal),
]