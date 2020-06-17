from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import FileResponse, HttpResponse

from datetime import date, datetime

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

def agendamentoHome(request):
    return render(request, 'institucional/agendamento.html')

def periodosDisponiveisHome(request):
    if request.method == "POST":
        
        if Data.dataVazia(request):
            return redirect('agendamentoHome')

        if Data.dataRetroativa(request):
            return redirect('agendamentoHome')
        
        if Periodo.foraDoPeriodoDeAtendimento(request):
            return redirect('agendamentoHome')

        contexto = Periodo.periodosDisponiveis(request)
        return render(request, 'institucional/agendamento.html', contexto)
    return render('agendamentoHome')

def cadastrarAgendamentoHome(request):      
    if request.method == "POST":
        if Agendamento.agendamentoUnico(request):
            return redirect('agendamentoHome')

        Agendamento.novoAgendamento(request)
        return redirect('agendamentoHome')
    return redirect('agendamentoHome')

def cancelarAgendamentoPorEmail(request, codigo_verificacao):
    contexto = Agendamento.statusAgendamento(codigo_verificacao)

    if request.method == 'POST':
        if request.POST['cancelar-agendamento'] == 'Sim':
            Agendamento.cancelarAgendamentoPorEmail(request, codigo_verificacao)
            contexto = Agendamento.statusAgendamento(codigo_verificacao)

    return render(request, 'institucional/cancelamento.html', contexto)

def avaliarAtendimento(request, codigo_verificacao):
    contexto = Avaliacao.atendimentoAvaliado(request, codigo_verificacao)

    if request.method == 'POST':
        Avaliacao.avaliarAtendimento(request, codigo_verificacao)

        contexto = Avaliacao.atendimentoAvaliado(request, codigo_verificacao)

    return render(request, 'institucional/avaliacao.html', contexto)


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

    contexto = {
        'usuarios_cadastrados' : Conta.usuariosCadastrados(),
        'estab_cadastrado' : Conta.estabelecimentoCadastrado(),
        'nome_usuario' : nome_usuario
    }

    return render(request, 'minha-conta/conta/lista.html', contexto)

def editarUsuario(request, id):
    if Login.verificarUsuarioLogado(request) == False:
        return redirect('acessoLogin')
    
    nome_usuario = request.session['nome_usuario_logado']   
    instancia_usuario = get_object_or_404(Usuario, id=id)
    
    if request.method == "POST":
        Conta.editarUsuario(request, id)

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
    servicos_cadastrados = Servico.objects.all()        

    busca = request.GET.get('search')
    if busca:
        servicos_cadastrados = Servicos.buscarServicoPeloNome(busca)
    
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
            Servicos.cadastrarServico(nome)
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

    busca = request.GET.get('search')
    if busca:
        contexto = {
                'agendamentos_cadastrados' : Agendamento.buscarAgendamentoPeloCliente(busca),
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
    if Login.verificarUsuarioLogado(request) == False:
        return redirect('acessoLogin')

    if request.method == "POST":
        if Agendamento.agendamentoUnico(request):
            return redirect('cadastrarAgendamento')

        Agendamento.novoAgendamento(request)
        return redirect('agendamentosCadastrados')

    contexto = {'nome_usuario' : nome_usuario}
    return render(request, 'minha-conta/agenda/cadastro.html', contexto)

def periodosDisponiveis(request):
    nome_usuario = request.session['nome_usuario_logado']
    if Login.verificarUsuarioLogado(request) == False:
        return redirect('acessoLogin')

    if request.method == "POST":
        request.session['origem-usuario'] = 'minha-conta'
        sessao = request.session['logado']
        nome_usuario = request.session['nome_usuario_logado']
        
        if Data.dataVazia(request):
            return redirect('cadastrarAgendamento')

        if Data.dataRetroativa(request):
            return redirect('cadastrarAgendamento')
        
        if Periodo.foraDoPeriodoDeAtendimento(request):
            return redirect('cadastrarAgendamento')

        contexto = Periodo.periodosDisponiveis(request)
        contexto.update({'nome_usuario' : request.session['nome_usuario_logado']})
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

# Subsistema: Relatório
def relatorios(request):
    if Login.verificarUsuarioLogado(request) == False:
            return redirect('acessoLogin')
        
    contexto = {
        'agendamentos_cadastrados' : Relatorio.agendamentosEfetuados(),
        'servicos_cadastrados' : Servicos.retornarListaServicos(),
        'nome_usuario' : request.session['nome_usuario_logado'],
        'relatorio_selecionado' : 'Todos'
    }

    if request.method == 'POST':
       contexto = Relatorio.filtrarRelatorio(request)
            
    return render(request, 'minha-conta/relatorio/lista.html', contexto)

def exportarRelatorio(request):
    nome_relatorio = request.POST['relatorio-selecionado'].replace(' ', '-')
    buffer = Relatorio.exportarRelatorio(request)
    return FileResponse(buffer, as_attachment=True, filename='Relatorio-{nome_relatorio}-{data}.xls'.format(nome_relatorio=nome_relatorio, data=Data.dataDoComputador('-')))