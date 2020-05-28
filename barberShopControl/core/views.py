from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import View
from django.core import serializers

import smtplib
import hashlib
import random
from email.mime.text import MIMEText
from datetime import date, datetime

from .forms import *
from .models import *
from .utils import *

# Login
def acessoLogin(request):
    if Login.verificarUsuarioLogado(request) == False:
        if request.method == 'POST':
            if Login.validarLogin(request):
                return redirect('dashboard')
            else:
                return redirect('acessoLogin')

        return render(request, 'login/acesso.html')

    return render(request, 'minha-conta/dashboard.html')

def deslogar(request):
    if Login.verificarUsuarioLogado(request) == False:
        return redirect('acessoLogin')
    
    if request.method == 'POST':
        request.session['usuario_logado'] = ''
        request.session['nome_usuario_logado'] = ''
        request.session['logado'] = False
        return redirect('acessoLogin')

    return redirect('acessoLogin')

def recuperarSenha(request):
    if Login.verificarUsuarioLogado(request) == False:

        if request.method == 'POST':
            retorno = Conta.validarRecuperacaoDeSenha(request)
            if retorno['status']:
                nova_senha = Senha.gerarSenhaRandomica()
                Usuario.objects.filter(us_usuario=retorno['usuario']).update(us_senha=nova_senha)
                Email.recuperarSenha(request, retorno['email'], retorno['especialista'], nova_senha)
        
        return render(request, 'login/recuperarsenha.html')

    return redirect('acessoLogin')

# Institucional
def home(request):
    return render(request, 'institucional/index.html')

def agendamento(request):
    return render(request, 'institucional/agendamento.html')

# Subsistema: Minha Conta
def dashboard(request):
    if Login.verificarUsuarioLogado(request) == False:
        return redirect('acessoLogin')
    
    nome_usuario = request.session['nome_usuario_logado']

    contexto = {
        'nome_usuario' : nome_usuario
    }
    return render(request, 'minha-conta/dashboard.html', contexto)

# Subsistema: Conta | Jurídica
def editarEstabelecimento(request, id):
    if Login.verificarUsuarioLogado(request) == False:
        return redirect('acessoLogin')
    
    nome_usuario = request.session['nome_usuario_logado']

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
        "instanciaEstabelecimento" : instanciaEstabelecimento,
        "form_estabelecimento" : form_estabelecimento,
        'nome_usuario' : nome_usuario
    }

    return render(request, 'minha-conta/conta/estabelecimento/editar.html', contexto)

# Subsistema: Serviço
def servicosCadastrados(request):
    if Login.verificarUsuarioLogado(request) == False:
        return redirect('acessoLogin')
    
    nome_usuario = request.session['nome_usuario_logado']
    
    # Trazendo todos os registros da tabela Serviço
    servicos_cadastrados = Servico.objects.all()        

    # Filtrando os registros da tabela Serviço
    busca = request.GET.get('search')
    if busca:
        servicos_cadastrados = Servico.objects.filter(serv_nome__icontains=busca)
    
    contexto = {
        'servicos_cadastrados' : servicos_cadastrados,
        'nome_usuario' : nome_usuario
    }

    return render(request, 'minha-conta/servicos/lista.html', contexto)

def cadastrarServico(request):
    if Login.verificarUsuarioLogado(request) == False:
        return redirect('acessoLogin')
    
    nome_usuario = request.session['nome_usuario_logado']
    form_servico = FormularioServico()
    if request.method == "POST":
        form_servico = FormularioServico(request.POST)
    
        if form_servico.is_valid():
            nome = form_servico.cleaned_data['serv_nome']
            valor = form_servico.cleaned_data['serv_valor']
            
            novo_servico = Servico(
                    serv_nome=nome, 
                    serv_valor=valor
                )

            novo_servico.save()
            messages.success(request, 'Serviço cadastrado com sucesso.', extra_tags='alert-success')
            return redirect('cadastrarServico')
        else:
            form_servico = FormularioServico()
            messages.success(request, 'Não foi possível cadastrar o serviço', extra_tags='alert-danger')

    contexto = {
        'form_servico' : form_servico,
        'nome_usuario' : nome_usuario
    }
    return render(request, 'minha-conta/servicos/cadastro.html', contexto)

def editarServico(request, id):
    if Login.verificarUsuarioLogado(request) == False:
        return redirect('acessoLogin')
    
    nome_usuario = request.session['nome_usuario_logado']
    
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
        "form_servico" : form_servico,
        'nome_usuario' : nome_usuario
    }
    return render(request, 'minha-conta/servicos/editar.html', contexto)

def excluirServico(request, id):
    if Login.verificarUsuarioLogado(request) == False:
        return redirect('acessoLogin')
    
    resultado_busca = Servico.objects.get(id=id)
    resultado_busca.delete()

    return redirect('servicosCadastrados')

# Subsistema: Conta | Física
def usuariosCadastrados(request):
    if Login.verificarUsuarioLogado(request) == False:
        return redirect('acessoLogin')
    
    nome_usuario = request.session['nome_usuario_logado']
    
    # Trazendo todos os registros da tabela Serviço
    usuarios_cadastrados = Usuario.objects.all()
    estab_cadastrado = Estabelecimento.objects.all()

    contexto = {
        'usuarios_cadastrados' : usuarios_cadastrados,
        'estab_cadastrado' : estab_cadastrado,
        'nome_usuario' : nome_usuario
    }

    return render(request, 'minha-conta/conta/lista.html', contexto)

def editarUsuario(request, id):
    if Login.verificarUsuarioLogado(request) == False:
        return redirect('acessoLogin')
    
    nome_usuario = request.session['nome_usuario_logado']
    
    instancia_usuario = get_object_or_404(Usuario, id=id)
    
    if request.method == "POST":
        nome = request.POST['nome-especialista']
        usuario = request.POST['usuario-especialista']
        senha = request.POST['senha-especialista']
        email = request.POST['email-especialista']

        Usuario.objects.filter(pk=id).update(us_nome=nome, us_usuario=usuario, us_senha=senha, us_email=email)

        # Mensagem de sucesso
        messages.success(request, 'Cadastro alterado com sucesso.', extra_tags='alert-success')
        
        instancia_usuario = get_object_or_404(Usuario, id=id)
        contexto = {
            "instancia_usuario" : instancia_usuario,
            'nome_usuario' : nome_usuario
        }
        return render(request, 'minha-conta/conta/editar.html', contexto)

    contexto = {
        "id_usuario_selecionado" : id,
        "instancia_usuario" : instancia_usuario,
        'nome_usuario' : nome_usuario
    }
    return render(request, 'minha-conta/conta/editar.html', contexto)

# Subsistema: Agenda
def agendamentosCadastrados(request):
    if Login.verificarUsuarioLogado(request) == False:
        return redirect('acessoLogin')

    Agendamento.agendamentoPendente()
    
    nome_usuario = request.session['nome_usuario_logado']

    agendamentos_cadastrados = Reserva.objects.filter(res_especialista=nome_usuario)    

    contexto = {
        'agendamentos_cadastrados' : agendamentos_cadastrados,
        'nome_usuario' : nome_usuario
    }
    return render(request, 'minha-conta/agenda/lista.html', contexto)

def cadastrarAgendamento(request):
    if request.session['origem-usuario'] == 'institucional':        
        if request.method == "POST":
            if Agendamento.agendamentoUnico(request):
                return redirect('agendamento')
            
            # Alterando o formato da data
            dia, mes, ano = Data.desmembrarData(request.POST['data-enviada'])
            data_formatada = '{ano}-{mes}-{dia}'.format(ano=ano, mes=mes, dia=dia)

            # Retirando os elementos do array e os separando por vírgula
            servicos = ', '.join(request.POST.getlist('servicos-selecionados'))

            # Salvando o novo agendamento
            novo_agendamento = Reserva(
                res_nome_cliente = request.POST['nome-cliente'],
                res_telefone_cliente = request.POST['telefone-cliente'],
                res_data_atendimento = data_formatada,
                res_periodo_atendimento = request.POST['periodo-atendimento'],
                res_email_cliente = request.POST['email-cliente'],
                res_especialista = request.POST['nome-especialista'],
                res_servicos = servicos,
                res_status = 'Ativo'
            )

            mensagem_agendamento_sucesso = """\
                Agendamento realizado com sucesso.
                Por favor, verifique o e-mail enviado para: {email}.
            """.format(email=request.POST['email-cliente'])

            messages.success(request, mensagem_agendamento_sucesso, extra_tags='alert-success')

            novo_agendamento.save()
            Email.novoAgendamento(request)
            return redirect('agendamento')
        
    else:
        nome_usuario = request.session['nome_usuario_logado']
        if request.method == "POST":
            if Login.verificarUsuarioLogado(request) == False:
                return redirect('acessoLogin')

            if Agendamento.agendamentoUnico(request):
                return redirect('cadastrarAgendamento')
            
            # Alterando o formato da data
            dia, mes, ano = Data.desmembrarData(request.POST['data-enviada'])
            data_formatada = '{ano}-{mes}-{dia}'.format(ano=ano, mes=mes, dia=dia)

            # Retirando os elementos do array e os separando por vírgula
            servicos = ', '.join(request.POST.getlist('servicos-selecionados'))

            # Salvando o novo agendamento
            novo_agendamento = Reserva(
                res_nome_cliente = request.POST['nome-cliente'],
                res_telefone_cliente = request.POST['telefone-cliente'],
                res_data_atendimento = data_formatada,
                res_periodo_atendimento = request.POST['periodo-atendimento'],
                res_email_cliente = request.POST['email-cliente'],
                res_especialista = request.POST['nome-especialista'],
                res_servicos = servicos,
                res_status = 'Ativo'
            )

            mensagem_agendamento_sucesso = """\
                Agendamento realizado com sucesso.
                Por favor, verifique o e-mail enviado para: {email}.
            """.format(email=request.POST['email-cliente'])

            messages.success(request, mensagem_agendamento_sucesso, extra_tags='alert-success')

            novo_agendamento.save()
            Email.novoAgendamento(request)
            return redirect('agendamentosCadastrados')

    contexto = {'nome_usuario' : nome_usuario}
    return render(request, 'minha-conta/agenda/cadastro.html', contexto)

def cancelarAgendamento(request, id_registro):
    if Login.verificarUsuarioLogado(request) == False:
        return redirect('acessoLogin')

    Email.cancelarAgendamento(request, id_registro)
    Reserva.objects.filter(id=id_registro).update(res_status='Cancelado')
    messages.success(request, 'Agendamento cancelado.', extra_tags='alert-success')
    return redirect('agendamentosCadastrados')

def periodosDisponiveis(request):
    if request.POST['origem-usuario'] == 'institucional':
        if request.method == "POST":
            request.session['origem-usuario'] = 'institucional'
            
            # Validando se a data não foi enviada vazia
            if Data.dataVazia(request):
                return redirect('agendamento')

            # Verificando se a data informada não é retroativa
            if Data.dataRetroativa(request):
                return redirect('agendamento')

            contexto = Periodo.periodosDisponiveis(request)
            return render(request, 'institucional/agendamento.html', contexto)
        
    else:
        if Login.verificarUsuarioLogado(request) == False:
            return redirect('acessoLogin')

        if request.method == "POST":
            request.session['origem-usuario'] = 'minha-conta'
            sessao = request.session['logado']
            nome_usuario = request.session['nome_usuario_logado']
            
            # Validando se a data não foi enviada vazia
            if Data.dataVazia(request):
                return redirect('cadastrarAgendamento')

            # Verificando se a data informada não é retroativa
            if Data.dataRetroativa(request):
                return redirect('cadastrarAgendamento')

            contexto = Periodo.periodosDisponiveis(request)
            return render(request, 'minha-conta/agenda/cadastro.html', contexto)

    contexto = {'nome_usuario' : nome_usuario}
    return render(request, 'minha-conta/agenda/cadastro.html', contexto)

def finalizarAgendamento(request):
    if Login.verificarUsuarioLogado(request) == False:
        return redirect('acessoLogin')

    if request.method == 'POST':
        nome_cliente  = request.POST['nome-cliente']
        email_destino = request.POST['email-cliente']
        data_agendada = request.POST['data-agendada']
        Email.finalizarAtendimento(email_destino, nome_cliente, data_agendada)
        Reserva.objects.filter(id=request.POST['id-registro']).update(res_observacao=request.POST['observacao-atendimento'], res_status='Finalizado')
    return redirect('agendamentosCadastrados')

