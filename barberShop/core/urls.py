from django.urls import path,reverse,include
from . import views as v


urlpatterns = [
    path('', v.index, name='index'),
    path("", include('django.contrib.auth.urls')),
    path('login/recuperarsenha/', v.recuperarSenha, name="recuperarSenha"),
    path('criarconta/', v.SignUp.as_view(), name="criarConta"),
    #path('criarconta/', v.cadastroUsuario, name="criarConta"),
    path("agenda.html/", v.agenda, name='agenda'),
    #path("login/cadastroUsuario/", v.cadastroUsuario, name='cadastroUsuario'),
] 