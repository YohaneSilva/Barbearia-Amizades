from django.urls import path

from . import views


urlpatterns = [
    # Institucional
    path('', views.home, name="home"),
    path('agendamento', views.agendamento, name="agendamento"),

    # Login
    path('login/', views.acessoLogin, name="acessoLogin"),
    path('login/recuperar-senha/', views.recuperarSenha, name="recuperarSenha"),

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
    path('minhaconta/conta/<int:id>/editar/', views.editarUsuario, name="editarUsuario"),

    # Conta Jurídica
    path('minhaconta/conta/<int:id>/editar/estabelecimento', views.editarEstabelecimento, name="editeditarEstabelecimentoarUsuario"),

    # Subsistema: Agenda
    path('minhaconta/agenda/', views.agendamentosCadastrados, name="agendamentosCadastrados"),
    path('minhaconta/agenda/novo-agendamento/', views.cadastrarAgendamento, name="cadastrarAgendamento"),
    path('minhaconta/agenda/novo-agendamento/#', views.periodosDisponiveis, name="periodosDisponiveis"),
    path('minhaconta/agenda/<int:id_registro>/', views.cancelarAgendamento, name="cancelarAgendamento"),
]