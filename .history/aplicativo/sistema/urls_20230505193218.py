from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views


urlpatterns = [
    path('registro', RegistroUsuario.as_view()),
    path('login', TokenObtainPairView.as_view()),
    path('perfil', Perfilusuario.as_view()),
    path('productos', ProductoView.as_view()),
    path('send/', views.Send.as_view(), name='send'),
]