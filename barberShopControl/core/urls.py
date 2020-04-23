from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.acesso, name="acesso"),
    path('login/recuperarsenha/', views.recuperarSenha, name="recuperarSenha"),
    path('login/criarconta/', views.criarConta, name="criarConta"),
    path('minhaconta/dashboard/', views.dashboard, name="dashboard"),
    path('minhaconta/servicos/cadastro', views.servicos, name="servicos"),
]