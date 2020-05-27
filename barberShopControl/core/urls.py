from django.urls import path

from . import views


urlpatterns = [
    # Institucional
    path('', views.home, name="home"),
    path('agendamento', views.agendamento, name="agendamento"),
    path('<slug:codigo_verificacao>', views.cancelarAgendamentoEmail, name="cancelarAgendamentoEmail"),
    path('<slug:codigo_verificacao>/avaliacao', views.avaliarAtendimento, name="avaliarAtendimento"),

    # Login
    path('login/', views.acessoLogin, name="acessoLogin"),
    path('login/recuperar-senha/', views.recuperarSenha, name="recuperarSenha"),

    # Deslogar 
    path('minhaconta/deslogar', views.deslogarMinhaConta, name="deslogarMinhaConta"),

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
    path('minhaconta/agenda/editar', views.finalizarCancelar, name="finalizarCancelar"),

    # Relatórios
    path('minhaconta/relatorio/', views.relatorios, name="relatorios"),
    path('minhaconta/relatorio/exportar', views.exportarRelatorio, name="exportarRelatorio"),
]