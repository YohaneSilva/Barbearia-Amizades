from django.urls import path

from . import views


urlpatterns = [
    # Institucional
    path('', views.home, name="home"),
    path('/agendamento', views.agendamento, name="agendamento"),
    path('/agendamento/#', views.periodosDisponiveisHome, name="periodosDisponiveisHome"),
    path('/agendamento/novo-agendamento', views.cadastrarAgendamentoHome, name="cadastrarAgendamentoHome"),

    # Login
    path('login/', views.acesso, name="acesso"),
    path('login/#', views.validarLogin, name="validarLogin"),
    path('login/recuperar-senha/', views.recuperarSenha, name="recuperarSenha"),
    path('login/criar-conta/', views.criarConta, name="criarConta"),

    # Deslogar 
    path('deslogar', views.deslogar, name="deslogar"),

    # Rota principal módulo admin
    path('minhaconta/dashboard/', views.dashboard, name="dashboard"),

    # Subsistema: Serviços
    path('minhaconta/servicos/', views.servicosCadastrados, name="servicosCadastrados"),
    path('minhaconta/servicos/cadastro/', views.cadastrarServico, name="cadastrarServico"),
    path('minhaconta/servicos/<int:id>/editar/', views.editarServico, name="editarServico"),
    path('minhaconta/servicos/<int:id>/', views.excluirServico, name="excluirServico"),

    # Subsistema: Conta
    path('minhaconta/conta/', views.usuariosCadastrados, name="usuariosCadastrados"),
    path('minhaconta/conta/cadastro/', views.cadastrarUsuario, name="cadastrarUsuario"),
    path('minhaconta/conta/<int:id>/editar/', views.editarUsuario, name="editarUsuario"),
    path('minhaconta/conta/<int:id>/', views.excluirUsuario, name="excluirUsuario"),

    # Conta Jurídica
    path('minhaconta/conta/<int:id>/editar/estabelecimento', views.editarEstabelecimento, name="editeditarEstabelecimentoarUsuario"),

    # Subsistema: Agenda
    path('minhaconta/agenda/', views.agendamentosCadastrados, name="agendamentosCadastrados"),
    path('minhaconta/agenda/novo-agendamento/', views.cadastrarAgendamento, name="cadastrarAgendamento"),
    path('minhaconta/agenda/novo-agendamento/#', views.periodosDisponiveis, name="periodosDisponiveis"),
    path('minhaconta/agenda/<int:id>/', views.excluirAgendamento, name="excluirAgendamento"),

    # Cadastrar estabelecimento automaticamente (alterar)
    path('minhaconta/conta/estab', views.cadastrarEstabelecimento, name="cadastrarEstabelecimento")
]