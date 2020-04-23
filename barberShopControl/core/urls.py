from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.acesso, name="acesso"),
    path('login/recuperarsenha/', views.recuperarSenha, name="recuperarSenha"),
    path('login/criarconta/', views.criarConta, name="criarConta"),
]