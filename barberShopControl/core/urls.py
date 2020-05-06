from django.urls import path

from . import views


urlpatterns = [
    path('login/', views.acesso, name="acesso"),
    path('login/recuperarsenha/', views.recuperarSenha, name="recuperarSenha"),
    path('login/criarconta/', views.criarConta, name="criarConta"),

    # Rota principal módulo admin
    path('minhaconta/dashboard/', views.dashboard, name="dashboard"),

    # Subsistema: Serviços
    path('minhaconta/servicos/', views.servicosCadastrados, name="servicosCadastrados"),
    path('minhaconta/servicos/cadastro/', views.cadastrarServico, name="cadastrarServico"),
    path('minhaconta/servicos/<int:id>/editar/', views.editarServico, name="editarServico"),
    path('minhaconta/servicos/<int:id>/', views.excluirServico, name="excluirServico"),

    # Subsistema: Conta
    path('minhaconta/conta/', views.contasCadastradas, name="contasCadastradas"),
    path('minhaconta/conta/cadastro/', views.cadastrarUsuario, name="cadastrarUsuario"),
    path('minhaconta/conta/<int:id>/editar/', views.editarUsuario, name="editarUsuario"),
    path('minhaconta/conta/<int:id>/', views.excluirUsuario, name="excluirUsuario"),

    # Cadastrar estabelecimento automaticamente (alterar)
    path('minhaconta/conta/estab', views.cadastrarEstabelecimento, name="cadastrarEstabelecimento"),
]