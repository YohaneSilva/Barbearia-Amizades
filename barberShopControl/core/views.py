from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .forms import *
from .filters import FiltroUsuario
from .models import Servico, Usuario

def acesso(request):
    return render(request, 'login/acesso.html')

def recuperarSenha(request):
    return render(request, 'login/recuperarsenha.html')

def criarConta(request):
    return render(request, 'login/criarconta.html')

def dashboard(request):
    return render(request, 'minha-conta/dashboard.html')

# Subsistema: Serviço
def servicosCadastrados(request):
    # Trazendo todos os registros da tabela Serviço
    servicos_cadastrados = Servico.objects.all()        

    # Filtrando os registros da tabela Serviço
    busca = request.GET.get('search')
    if busca:
        servicos_cadastrados = Servico.objects.filter(serv_nome__icontains=busca)
    
    contexto = {'servicos_cadastrados' : servicos_cadastrados}

    return render(request, 'minha-conta/servicos/lista.html', contexto)

def cadastrarServico(request):
    form_servico = FormularioServico()

    if request.method == "POST":
        form_servico = FormularioServico(request.POST)
    
        if form_servico.is_valid():
            nome = form_servico.cleaned_data['serv_nome']
            tempo_duracao = form_servico.cleaned_data['serv_tempo_duracao']
            valor = form_servico.cleaned_data['serv_valor']
            
            novo_servico = Servico(
                    serv_nome=nome, 
                    serv_tempo_duracao=tempo_duracao, 
                    serv_valor=valor
                )

            novo_servico.save()

            messages.success(request, 'Serviço cadastrado com sucesso.', extra_tags='alert-success')

            return redirect('cadastrarServico')

        else:
            form_servico = FormularioServico()
            messages.success(request, 'Não foi possível cadastrar o serviço', extra_tags='alert-danger')
    
    contexto = {'form_servico' : form_servico}

    return render(request, 'minha-conta/servicos/cadastro.html', contexto)

def editarServico(request, id):
    instanciaServico = get_object_or_404(Servico, id=id)
    
    if request.method == "POST":
        form_servico = FormularioServico(request.POST, instance=instanciaServico)

        if form_servico.is_valid():
            instanciaServico = form_servico.save(commit=False)
            instanciaServico.save()

            # Mensagem de sucesso
            messages.success(request, 'Serviço alterado com sucesso.', extra_tags='alert-success')
        else:
            messages.error(request, 'Serviço não alterado.', extra_tags='alert-danger')
    else:
        form_servico = FormularioServico(instance=instanciaServico)

    contexto = {
        "id_servico_selecionado" : id,
        "instanciaServico" : instanciaServico,
        "form_servico" : form_servico
    }
    return render(request, 'minha-conta/servicos/editar.html', contexto)

def excluirServico(request, id):
    if request.method == "POST":
        instance = Servico.objects.get(id=id)
        instance.delete()
        messages.success(request, 'Serviço excluído com sucesso.', extra_tags='alert-success')
        return redirect('servicosCadastrados')


# Subsistema: Conta
def usuariosCadastrados(request):
    # Trazendo todos os registros da tabela Serviço
    usuarios_cadastrados = Usuario.objects.all()

    filtro_usuarios_cadastrados = FiltroUsuario(request.GET, queryset=usuarios_cadastrados)
    usuarios_cadastrados = filtro_usuarios_cadastrados.qs

    contexto = {
        'usuarios_cadastrados' : usuarios_cadastrados,
        'filtro_usuarios_cadastrados' : filtro_usuarios_cadastrados,
    }

    return render(request, 'minha-conta/conta/lista.html', contexto)

def cadastrarUsuario(request):
    form_usuario = FormularioConta()

    if request.method == "POST":
        form_usuario = FormularioConta(request.POST)
        
        if form_usuario.is_valid():
            status = form_usuario.cleaned_data['us_situacao_conta']
            perfil = form_usuario.cleaned_data['us_perfil']
            nome = form_usuario.cleaned_data['us_primeiro_nome']
            sobrenome = form_usuario.cleaned_data['us_segundo_nome']
            sexo = form_usuario.cleaned_data['us_sexo']
            email = form_usuario.cleaned_data['us_email']
            telefone = form_usuario.cleaned_data['us_telefone']

            novo_usuario = Usuario(
                    us_situacao_conta=status,
                    us_perfil=perfil, 
                    us_primeiro_nome=nome, 
                    us_segundo_nome=sobrenome, 
                    us_sexo=sexo,
                    us_email=email,
                    us_telefone=telefone
                )

            novo_usuario.save()

            messages.success(request, 'Cadastro realizado com sucesso.', extra_tags='alert-success')
            return redirect('cadastrarUsuario')

        else:
            form_usuario = FormularioConta()
            messages.success(request, 'Não foi possível cadastrar o usuário', extra_tags='alert-danger')
    
    contexto = {'form_usuario' : form_usuario}

    return render(request, 'minha-conta/conta/cadastro.html', contexto)

def editarUsuario(request, id):
    instanciaUsuario = get_object_or_404(Usuario, id=id)
    
    if request.method == "POST":
        form_usuario = FormularioConta(request.POST, instance=instanciaUsuario)

        if form_usuario.is_valid():
            instanciaUsuario = form_usuario.save(commit=False)
            instanciaUsuario.save()

            # Mensagem de sucesso
            messages.success(request, 'Cadastro alterado com sucesso.', extra_tags='alert-success')
        else:
            messages.error(request, 'Cadastro não alterado.', extra_tags='alert-danger')
    else:
        form_usuario = FormularioConta(instance=instanciaUsuario)

    contexto = {
        "id_usuario_selecionado" : id,
        "instanciaUsuario" : instanciaUsuario,
        "form_usuario" : form_usuario
    }
    return render(request, 'minha-conta/conta/editar.html', contexto)

def excluirUsuario(request, id):
    if request.method == "POST":
        instance = Usuario.objects.get(id=id)
        instance.delete()
        messages.success(request, 'Cadastro excluído', extra_tags='alert-success')
        return redirect('usuariosCadastrados')