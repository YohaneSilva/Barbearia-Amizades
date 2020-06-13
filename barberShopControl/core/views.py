from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import View
from django.core import serializers
from django.http import FileResponse, HttpResponse

import io
import smtplib
import hashlib
import random
import xlwt
from email.mime.text import MIMEText
from datetime import date, datetime
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from .forms import *
from .utils import *

# Login
def acessoLogin(request):
    if Login.verificarUsuarioLogado(request) == True:
        return redirect('dashboard')
    
    if request.method == 'POST':
        if Login.validarLogin(request):
            return redirect('dashboard')
    
    return render(request, 'login/acesso.html')

def deslogarMinhaConta(request):
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

    return render(request, 'login/recuperarsenha.html')

# Institucional
def home(request):
    return render(request, 'institucional/index.html')

def agendamento(request):
    return render(request, 'institucional/agendamento.html')

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

# Subsistema: Minha Conta
def dashboard(request):   
    if Login.verificarUsuarioLogado(request) == False:
        return redirect('acessoLogin')
    
    nome_usuario = request.session['nome_usuario_logado']

    total_agendamento_chiquinho = Relatorio.totalAgendamentosChiquinho()
    total_agendamento_sandrinho = Relatorio.totalAgendamentosSandrinho()
    total_agendamentos_ativos = Relatorio.totalAgendamentosAtivos()
    total_agendamentos_cancelados = Relatorio.totalAgendamentosCancelados()
    total_agendamentos_finalizados = Relatorio.totalAgendamentosFinalizados()
    total_agendamentos_pendentes = Relatorio.totalAgendamentosPendentes()
    total_agendamentos_mes = Relatorio.totalAgendamentosDoMes()
    total_agendamentos_ano = Relatorio.totalAgendamentosDoAno()
    total_agendamentos = Relatorio.totalAgendamentos()
    total_agendamentos_por_servico = Relatorio.totalAgendamentoPorServico()

    contexto = {
        'nome_usuario' : nome_usuario,
        'total_agendamento_chiquinho' : total_agendamento_chiquinho,
        'total_agendamento_sandrinho' : total_agendamento_sandrinho,
        'total_agendamentos_ativos' : total_agendamentos_ativos,
        'total_agendamentos_cancelados' : total_agendamentos_cancelados,
        'total_agendamentos_finalizados' : total_agendamentos_finalizados,
        'total_agendamentos_pendentes' : total_agendamentos_pendentes,
        'total_agendamentos_mes' : total_agendamentos_mes,
        'total_agendamentos' : total_agendamentos,
        'total_agendamentos_ano' : total_agendamentos_ano,
        'total_agendamentos_por_servico': total_agendamentos_por_servico
    }
    return render(request, 'minha-conta/dashboard.html', contexto)

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

def habilitarDesabilitarServico(request, id):
    if Login.verificarUsuarioLogado(request) == False:
        return redirect('acessoLogin')

    Servicos.atualizarStatus(id)
    return redirect('servicosCadastrados')

# Subsistema: Agenda
def agendamentosCadastrados(request):
    if Login.verificarUsuarioLogado(request) == False:
        return redirect('acessoLogin')

    Agendamento.agendamentoPendente()
    nome_usuario = request.session['nome_usuario_logado']

    contexto = {
        'agendamentos_cadastrados' : Agendamento.todosAgendamentos(nome_usuario),
        'nome_usuario' : nome_usuario,
        'relatorio_selecionado' : 'Todos'
    }

    if request.method == 'POST':
        if request.POST['mes-selecionado'] != 'Todos':
            contexto = {
                'agendamentos_cadastrados' : Relatorio.agendamentosPorMes(request.POST['mes-selecionado']),
                'nome_usuario' : nome_usuario,
                'relatorio_selecionado' : Data.mesDoAno(request.POST['mes-selecionado'])
            }

    return render(request, 'minha-conta/agenda/lista.html', contexto)

def cadastrarAgendamento(request):
    nome_usuario = request.session['nome_usuario_logado']
    if request.session['origem-usuario'] == 'institucional':        
        if request.method == "POST":
            if Agendamento.agendamentoUnico(request):
                return redirect('agendamento')
            
            # Alterando o formato da data
            dia, mes, ano = Data.desmembrarData(request.POST['data-enviada'])
            data_formatada = '{ano}-{mes}-{dia}'.format(ano=ano, mes=mes, dia=dia)

            # Retirando os elementos do array e os separando por vírgula
            servicos = ', '.join(request.POST.getlist('servicos-selecionados'))
            codigo_verificacao = Senha.gerarSenhaRandomica()

            # Salvando o novo agendamento
            novo_agendamento = Reserva(
                res_nome_cliente = request.POST['nome-cliente'],
                res_telefone_cliente = request.POST['telefone-cliente'],
                res_data_atendimento = data_formatada,
                res_periodo_atendimento = request.POST['periodo-atendimento'],
                res_email_cliente = request.POST['email-cliente'],
                res_especialista = request.POST['nome-especialista'],
                res_servicos = servicos,
                res_status = 'Ativo',
                res_codigo_verificacao = codigo_verificacao,
                res_observacao = request.POST['observacao-atendimento']
            )

            mensagem_agendamento_sucesso = """\
                Agendamento realizado com sucesso.
                Por favor, verifique o e-mail enviado para: {email}.
            """.format(email=request.POST['email-cliente'])

            messages.success(request, mensagem_agendamento_sucesso, extra_tags='alert-success')

            novo_agendamento.save()
            Email.novoAgendamento(request, codigo_verificacao)
            return redirect('agendamento')
        
    else:
        nome_usuario = request.session['nome_usuario_logado']
        if Login.verificarUsuarioLogado(request) == False:
            return redirect('acessoLogin')

        if request.method == "POST":

            if Agendamento.agendamentoUnico(request):
                return redirect('cadastrarAgendamento')
            
            # Alterando o formato da data
            dia, mes, ano = Data.desmembrarData(request.POST['data-enviada'])
            data_formatada = '{ano}-{mes}-{dia}'.format(ano=ano, mes=mes, dia=dia)

            # Retirando os elementos do array e os separando por vírgula
            servicos = ', '.join(request.POST.getlist('servicos-selecionados'))
            codigo_verificacao = Senha.gerarSenhaRandomica()

            # Salvando o novo agendamento
            novo_agendamento = Reserva(
                res_nome_cliente = request.POST['nome-cliente'],
                res_telefone_cliente = request.POST['telefone-cliente'],
                res_data_atendimento = data_formatada,
                res_periodo_atendimento = request.POST['periodo-atendimento'],
                res_email_cliente = request.POST['email-cliente'],
                res_especialista = request.POST['nome-especialista'],
                res_servicos = servicos,
                res_status = 'Ativo',
                res_codigo_verificacao = codigo_verificacao,
                res_observacao = request.POST['observacao-atendimento']
            )

            mensagem_agendamento_sucesso = """\
                Agendamento realizado com sucesso.
                Por favor, verifique o e-mail enviado para: {email}.
            """.format(email=request.POST['email-cliente'])

            messages.success(request, mensagem_agendamento_sucesso, extra_tags='alert-success')

            novo_agendamento.save()
            Email.novoAgendamento(request, codigo_verificacao)
            return redirect('agendamentosCadastrados')

        contexto = {'nome_usuario' : nome_usuario}
        return render(request, 'minha-conta/agenda/cadastro.html', contexto)

    contexto = {'nome_usuario' : nome_usuario}
    return render(request, 'minha-conta/agenda/cadastro.html', contexto)

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

def finalizarCancelar(request):
    if Login.verificarUsuarioLogado(request) == False:
            return redirect('acessoLogin')
    
    if request.method == 'POST':
        if 'finalizar-atendimento' in request.POST:
            Agendamento.finalizarAgendamento(request)

        if 'cancelar-atendimento' in request.POST:
            Agendamento.cancelarAgendamento(request)
        
    return redirect('agendamentosCadastrados')

def cancelarAgendamentoEmail(request, codigo_verificacao):
    reserva = Reserva.objects.filter(res_codigo_verificacao=codigo_verificacao)
    
    contexto = {
        'status' : True,
        'reserva' : reserva
    }

    for item in reserva:
        nome_cliente = getattr(item, 'res_nome_cliente')
        data_atendimento = getattr(item, 'res_data_atendimento')
        especialista = getattr(item, 'res_especialista')

        if getattr(item, 'res_status') == 'Ativo':
            contexto = {
                'status' : False,
                'reserva' : reserva
            }
        else:
            contexto = {
                'status' : True,
                'reserva' : reserva
            }

    if request.method == 'POST':
        for resultado in request.POST:
            if request.POST[resultado] == 'Sim':
                messages.success(request, 'Agendamento cancenlado com sucesso. Por favor, verique seu e-mail.', extra_tags='alert-success')
                reserva.update(res_status='Cancelado pelo usuário')
                Email.cancelarAgendamento(request, getattr(item, 'id'))
                contexto = {
                    'status' : True,
                    'reserva' : reserva
                }

        return render(request, 'institucional/cancelamento.html', contexto)
    return render(request, 'institucional/cancelamento.html', contexto)

def avaliarAtendimento(request, codigo_verificacao):
    reserva = Reserva.objects.filter(res_codigo_verificacao=codigo_verificacao)
    
    # http://127.0.0.1:8000/hhtfea3Gcg/avaliacao

    contexto = {
        'status' : False,
        'reserva' : reserva
    }

    if Agendamento.agendamentoNaoFinalizado(reserva, codigo_verificacao):
        return redirect('home')

    for item in reserva:
        if getattr(item, 'res_avaliacao') > 0:
            contexto = {
                'status' : True,
                'reserva' : reserva
            }

    if request.method == 'POST':
        reserva.update(res_avaliacao=int(request.POST['avaliacao_cliente']), res_observacao_avaliacao=request.POST['observacao-avaliacao'])
        messages.success(request, 'Obrigado pela avaliação!', extra_tags='alert-success')

        contexto = {
            'status' : True,
            'reserva' : reserva
        }

    return render(request, 'institucional/avaliacao.html', contexto)

# Subsistema: Relatório
def relatorios(request):
    if Login.verificarUsuarioLogado(request) == False:
        return redirect('acessoLogin')

    contexto = {
        'agendamentos_cadastrados' : Reserva.objects.all(),
        'servicos_cadastrados' : Servicos.retornarListaServicos(),
        'nome_usuario' : request.session['nome_usuario_logado'],
        'relatorio_selecionado' : 'Todos'
    }

    if request.method == 'POST':
        for valor in request.POST:
            if request.POST[valor] == 'Agendamentos do Mês':
                contexto = {
                    'agendamentos_cadastrados' : Relatorio.agendamentosDoMes(),
                    'servicos_cadastrados' : Servicos.retornarListaServicos(),
                    'nome_usuario' : request.session['nome_usuario_logado'],
                    'relatorio_selecionado' : 'Agendamentos do Mês'
                }

            if request.POST[valor] == 'Agendamentos Ativos':
                contexto = {
                    'agendamentos_cadastrados' : Relatorio.agendamentosAtivos(),
                    'servicos_cadastrados' : Servicos.retornarListaServicos(),
                    'nome_usuario' : request.session['nome_usuario_logado'],
                    'relatorio_selecionado' : 'Agendamentos Ativos'
                }
            
            if request.POST[valor] == 'Agendamentos Finalizados':
                contexto = {
                    'agendamentos_cadastrados' : Relatorio.agendamentosFinalizados(),
                    'servicos_cadastrados' : Servicos.retornarListaServicos(),
                    'nome_usuario' : request.session['nome_usuario_logado'],
                    'relatorio_selecionado' : 'Agendamentos Finalizados'
                }
            
            if request.POST[valor] == 'Agendamentos Pendentes':
                contexto = {
                    'agendamentos_cadastrados' : Relatorio.agendamentosPendentes(),
                    'servicos_cadastrados' : Servicos.retornarListaServicos(),
                    'nome_usuario' : request.session['nome_usuario_logado'],
                    'relatorio_selecionado' : 'Agendamentos Pendentes'
                }
            
            if request.POST[valor] == 'Agendamentos Cancelados':
                contexto = {
                    'agendamentos_cadastrados' : Relatorio.agendamentosCancelados(),
                    'servicos_cadastrados' : Servicos.retornarListaServicos(),
                    'nome_usuario' : request.session['nome_usuario_logado'],
                    'relatorio_selecionado' : 'Agendamentos Cancelados'
                }
            
            if request.POST[valor] == 'Agendamentos Cancelados Pelo Usuário':
                contexto = {
                    'agendamentos_cadastrados' : Relatorio.agendamentosCanceladosPeloUsuario(),
                    'servicos_cadastrados' : Servicos.retornarListaServicos(),
                    'nome_usuario' : request.session['nome_usuario_logado'],
                    'relatorio_selecionado' : 'Agendamentos Cancelados Pelo Usuário'
                }
            
            if request.POST[valor] == 'Agendamentos Cancelados Pelo Especialista':
                contexto = {
                    'agendamentos_cadastrados' : Relatorio.agendamentosCanceladosPeloEspecialista(),
                    'servicos_cadastrados' : Servicos.retornarListaServicos(),
                    'nome_usuario' : request.session['nome_usuario_logado'],
                    'relatorio_selecionado' : 'Agendamentos Cancelados Pelo Especialista'
                }
            
            if request.POST[valor] in 'Chiquinho Oliveira':
                contexto = {
                    'agendamentos_cadastrados' : Relatorio.agendamentosEspecialista('Chiquinho Oliveira'),
                    'servicos_cadastrados' : Servicos.retornarListaServicos(),
                    'nome_usuario' : request.session['nome_usuario_logado'],
                    'relatorio_selecionado' : 'Agendamentos por Especialista: {especialista}'.format(especialista='Chiquinho Oliveira')
                }
            
            if request.POST[valor] in 'Sandrinho Santos':
                contexto = {
                    'agendamentos_cadastrados' : Relatorio.agendamentosEspecialista('Sandrinho Santos'),
                    'servicos_cadastrados' : Servicos.retornarListaServicos(),
                    'nome_usuario' : request.session['nome_usuario_logado'],
                    'relatorio_selecionado' : 'Agendamentos por Especialista: {especialista}'.format(especialista='Sandrinho Santos')
                }

            if request.POST[valor] in Servicos.retornarListaServicos():
                contexto = {
                    'agendamentos_cadastrados' : Relatorio.agendamentosPorServico(request.POST[valor]),
                    'servicos_cadastrados' : Servicos.retornarListaServicos(),
                    'nome_usuario' : request.session['nome_usuario_logado'],
                    'relatorio_selecionado' : 'Agendamentos por Serviço: {servico}'.format(servico=request.POST[valor])
                }
            

    return render(request, 'minha-conta/relatorio/lista.html', contexto)

def exportarRelatorio(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the Exel
    workbook = xlwt.Workbook()
    # add data

    # save to buffer
    workbook.save(buffer)

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='example.xls')

'''
pdf = io.BytesIO()

doc = SimpleDocTemplate(pdf, pagesize=letter)
# container for the 'Flowable' objects
elements = []
data= [[
    'Código', 
    'Agendado Em', 
    'Nome', 
    'Telefone', 
    'E-mail', 
    'Data Atendimento', 
    'Especialista', 
    'Período Atendimento',
    'Serviço',
    'Situação',
    'Observação'
],
['10', '11', '12', '13', '14'],
['20', '21', '22', '23', '24'],
['30', '31', '32', '33', '34']]
t=Table(data,20*[0.7*inch], 4*[0.7*inch])
t.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
    ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
    ('VALIGN',(0,0),(0,-1),'TOP'),
    ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
    ('ALIGN',(0,-1),(-1,-1),'CENTER'),
    ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
    ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
]))

elements.append(t)
# write the document to disk
doc.build(elements)
pdf.seek(0)

return FileResponse(pdf, as_attachment=True, filename='relatorio-{nomeRelatorio}.pdf'.format(nomeRelatorio=''))

<QueryDict: {
    'csrfmiddlewaretoken': ['y3kcXNY783lykVTaAt9yMeWUvQnmFHERorSGKDl79qMywO6ZmamlXqbr4S2yFC0K'], 
    'codigo': ['61'], 
    'agendado-em': ['8 de Junho de 2020 às 16:37'], 
    'nome-cliente': ['Luciana dos Santos'], 
    'telefone-cliente': ['11123231312'], 
    'email-cliente': ['lenildo.ln@gmail.com'], 
    'data-atendimento': ['9 de Junho de 2020'], 
    'nome-especialista': ['Sandrinho Santos'], 
    'periodo-atendimento': ['9-10'], 
    'servicos': [''], 
    'status-atendimento': ['Cancelado pelo usuário'], 
    'observacao-agendamento': [' '], 
    'avaliacao-cliente': ['Sem avaliação'], 
    'observacao-avaliacao-cliente': [''], 
    'observacao-especialista': ['']
    }>
'''