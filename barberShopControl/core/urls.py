from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.loginPrincipal, name="loginPrincipal"),
    path('login/recuperarsenha/', views.recuperarSenha, name="recuperarSenha"),
    path('login/criarconta/', views.criarConta, name="criarConta"),
    path('minhaconta/dashboard/', views.dashboar, name="dashboard"),
    path('minhaconta/servicos/', views.servicos, name="servicos"),
]