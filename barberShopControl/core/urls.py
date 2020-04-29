from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.entrar, name="entrar"),
    path('criarconta/', views.criarConta, name="criarConta"),
    path('login/recuperarsenha/', views.recuperarSenha, name="recuperarSenha"),
]
