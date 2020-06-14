from django.urls import path

from . import views


urlpatterns = [
    # Institucional
    path('', views.home, name="home"),
    path('agendamento/', views.agendamento, name="agendamento"),
    path('<slug:codigo_verificacao>/cancelamento/', views.cancelarAgendamentoPorEmail, name="cancelarAgendamentoPorEmail"),
    path('<slug:codigo_verificacao>/avaliacao/', views.avaliarAtendimento, name="avaliarAtendimento"),

    # Login
    path('login/', views.acessoLogin, name="acessoLogin"),
    path('login/recuperar-senha/', views.recuperarSenha, name="recuperarSenha"),

    # Deslogar 
    path('minha-conta/deslogar/', views.deslogarMinhaConta, name="deslogarMinhaConta"),

    # Rota principal módulo admin
    path('minha-conta/dashboard/', views.dashboard, name="dashboard"),

    # Subsistema: Serviços
    path('minha-conta/servicos/', views.servicosCadastrados, name="servicosCadastrados"),
    path('minha-conta/servicos/cadastro/', views.cadastrarServico, name="cadastrarServico"),
    path('minha-conta/servicos/<int:id>/editar/', views.editarServico, name="editarServico"),
    path('minha-conta/servicos/<int:id>/', views.habilitarDesabilitarServico, name="habilitarDesabilitarServico"),

    # Subsistema: Conta
    path('minha-conta/conta/', views.usuariosCadastrados, name="usuariosCadastrados"),
    path('minha-conta/conta/<int:id>/editar/', views.editarUsuario, name="editarUsuario"),

    # Conta Jurídica
    path('minha-conta/conta/<int:id>/editar/estabelecimento/', views.editarEstabelecimento, name="editeditarEstabelecimentoarUsuario"),

    # Subsistema: Agenda
    path('minha-conta/agenda/', views.agendamentosCadastrados, name="agendamentosCadastrados"),
    path('minha-conta/agenda/novo-agendamento/', views.cadastrarAgendamento, name="cadastrarAgendamento"),
    path('minha-conta/agenda/novo-agendamento/#', views.periodosDisponiveis, name="periodosDisponiveis"),
    path('minha-conta/agenda/editar/', views.finalizarCancelar, name="finalizarCancelar"),

    # Relatórios
    path('minha-conta/relatorio/', views.relatorios, name="relatorios"),
    path('minha-conta/relatorio/exportar/', views.exportarRelatorio, name="exportarRelatorio"),
]