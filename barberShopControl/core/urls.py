from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login, name="login"),
    path('login/recuperarsenha/', views.recuperarSenha, name="recuperarSenha"),
    path('login/cadastro/', views.cadastroCliente, name="cadastroCliente"),
]