from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .forms import *
from .filters import FiltroUsuario
from .models import Servico, Usuario, Estabelecimento

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

def contasCadastradas(request):
    # Trazendo todos os registros da tabela Serviço
    usuarios_cadastrados = Usuario.objects.all()
    estab_cadastrado = Estabelecimento.objects.all()

    # Filtros
    # filtro_usuarios_cadastrados = Filtro(request.GET, queryset=usuarios_cadastrados)
    # usuarios_cadastrados = filtro_usuarios_cadastrados.qs

    contexto = {
        'usuarios_cadastrados' : usuarios_cadastrados,
        'estab_cadastrado' : estab_cadastrado
    }

    return render(request, 'minha-conta/conta/lista.html', contexto)

# Conta Jurídica
def editarContaJuridica(request, id):
    instanciaEstabelecimento = get_object_or_404(Estabelecimento, id=id)
    
    if request.method == "POST":
        form_estabelecimento = FormularioEstabelecimento(request.POST, instance=instanciaEstabelecimento)

        if form_estabelecimento.is_valid():
            instanciaEstabelecimento = form_estabelecimento.save(commit=False)
            instanciaEstabelecimento.save()

            # Mensagem de sucesso
            messages.success(request, 'Cadastro alterado com sucesso.', extra_tags='alert-success')
        else:
            messages.error(request, 'Cadastro não alterado.', extra_tags='alert-danger')
    else:
        form_estabelecimento = FormularioEstabelecimento(instance=instanciaEstabelecimento)

    contexto = {
        "id_usuario_selecionado" : id,
        "instanciaEstabelecimento" : instanciaEstabelecimento,
        "form_estabelecimento" : form_estabelecimento
    }

    return render(request, 'minha-conta/conta/editar.html', contexto)

# Cadastrar Estabelecimento
def cadastrarEstabelecimento(request):

    novo_usuario = Estabelecimento(
            estab_cnpj='42157458000107',
            estab_razao_social='Sandoval Santos Silva Filho',
            estab_nome_fantasia='Barbearia Amizades S & D',
            estab_end_cep='13232281',
            estab_end_logradouro='R. Edmundo Antônio Pernetti',
            estab_end_numero='212',
            estab_end_complemento='2º andar',
            estab_end_bairro='Jardim Santo Antonio I',
            estab_end_cidade='Campo Limpo Paulista',
            estab_end_uf='SP'
        )

    novo_usuario.save()

    return redirect('contasCadastradas')

def cadastrarUsuario(request):
    form_usuario = FormularioUsuario()    

    if request.method == "POST":
        form_usuario = FormularioUsuario(request.POST)
        
        if form_usuario.is_valid():
            status = form_usuario.cleaned_data['us_situacao_conta']
            nome = form_usuario.cleaned_data['us_primeiro_nome']
            sobrenome = form_usuario.cleaned_data['us_segundo_nome']
            sexo = form_usuario.cleaned_data['us_sexo']
            email = form_usuario.cleaned_data['us_email']
            telefone = form_usuario.cleaned_data['us_telefone']

            novo_usuario = Usuario(
                    us_situacao_conta=status,
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
            form_usuario = FormularioUsuario()
            messages.success(request, 'Não foi possível cadastrar o usuário', extra_tags='alert-danger')
    
    contexto = {'form_usuario' : form_usuario}

    return render(request, 'minha-conta/conta/cadastro.html', contexto)

def editarUsuario(request, id):
    instanciaUsuario = get_object_or_404(Usuario, id=id)
    
    if request.method == "POST":
        form_usuario = FormularioUsuario(request.POST, instance=instanciaUsuario)

        if form_usuario.is_valid():
            instanciaUsuario = form_usuario.save(commit=False)
            instanciaUsuario.save()

            # Mensagem de sucesso
            messages.success(request, 'Cadastro alterado com sucesso.', extra_tags='alert-success')
        else:
            messages.error(request, 'Cadastro não alterado.', extra_tags='alert-danger')
    else:
        form_usuario = FormularioUsuario(instance=instanciaUsuario)

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
        return redirect('contasCadastradas')