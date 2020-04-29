from django.urls import path

from . import views


urlpatterns = [
    path('login/', views.acesso, name="acesso"),
    path('login/recuperarsenha/', views.recuperarSenha, name="recuperarSenha"),
    path('login/criarconta/', views.criarConta, name="criarConta"),
    path('minhaconta/dashboard/', views.dashboard, name="dashboard"),
    path('minhaconta/servicos/todos/', views.servicosCadastrados, name="servicosCadastrados"),
    path('minhaconta/servicos/cadastro/', views.novoServico, name="novoServico"),
    path('minhaconta/servicos/<int:id>/editar/', views.editarServico, name="editarServico"),
    path('minhaconta/servicos/editar/', views.editarServico, name="editarServico"),
    path('minhaconta/servicos/todos/<int:id>/', views.excluirServico, name="excluirServico"),
]