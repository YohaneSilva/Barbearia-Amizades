from django.urls import path,reverse
from . import views as v


urlpatterns = [
    path('', v.index, name='index'),
    path("login/", v.login, name='acesso'),
    path('login/recuperarsenha/', v.recuperarSenha, name="recuperarSenha"),
    path('login/criarconta/', v.cadastroUsuario, name="criarConta"),
    path("agenda.html/", v.agenda, name='agenda'),
    #path("login/cadastroUsuario/", v.cadastroUsuario, name='cadastroUsuario'),
]