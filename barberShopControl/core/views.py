from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import View

import datetime
from datetime import date

from .forms import *
from .models import *

def acesso(request):
    return render(request, 'login/acesso.html')

def recuperarSenha(request):
    return render(request, 'login/recuperarsenha.html')

def criarConta(request):
    return render(request, 'login/criarconta.html')

def dashboard(request):
    return render(request, 'minha-conta/dashboard.html')


### Cadastrar Estabelecimento | Apenas para TESTE
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

### Conta Jurídica
def editarEstabelecimento(request, id):
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
        "form_estabelecimento" : form_estabelecimento
    }

    return render(request, 'minha-conta/conta/estabelecimento/editar.html', contexto)

def cadastrarUsuario(request):
    form_usuario = FormularioUsuario()

    if request.method == "POST":
        form_usuario = FormularioUsuario(request.POST)
        
        if form_usuario.is_valid():
            nome = form_usuario.cleaned_data['us_nome']
            usuario = form_usuario.cleaned_data['us_usuario']
            senha = form_usuario.cleaned_data['us_senha']

            novo_usuario = Usuario(
                    us_nome=nome,
                    us_usuario=usuario, 
                    us_senha=senha, 
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

def agendamentosCadastrados(request):
    agendamentos_cadastrados = Reserva.objects.all()

    contexto = {
        'agendamentos_cadastrados' : agendamentos_cadastrados
    }

    return render(request, 'minha-conta/agenda/lista.html', contexto)

def cadastrarAgendamento(request):
    if request.method == "POST":
    
        # Separando a data por dia, mês e ano
        data = request.POST['data_selecionada']
        data = data.replace('/', ' ')
        dia = int(data.split()[0])
        mes = int(data.split()[1])
        ano = int(data.split()[2]) 
        
        # Verificando se o mesmo cliente já não possui 
        # um agendamento na data selecionada
        reservas = Reserva.objects.filter(res_data_atendimento=datetime.date(ano, mes, dia))
        if len(reservas.values()) > 0:
            for index in range(len(reservas.values())):
                nome_cliente = reservas.values()[index]['res_nome_cliente']

                if nome_cliente == request.POST['nome-cliente']:
                    messages.success(request, 'Você já possui um agendamento na data selecionada.', extra_tags='alert-danger')
                    return redirect('cadastrarAgendamento')


        # Validando a quantidade caracteres
        # do telefone
        telefone = request.POST['telefone-cliente']
        if len(telefone) > 11:
            messages.success(request, 'Os dados informados estão incorretos.', extra_tags='alert-danger')
            return redirect('cadastrarAgendamento')
        
        # Alterando o formato da data
        data_formatada = '{ano}-{mes}-{dia}'.format(ano=ano, mes=mes, dia=dia)

        # Retirando os elementos do array e os separando por vírgula
        servicos = ', '.join(request.POST.getlist('servicos-selecionados'))

        novo_agendamento = Reserva(
            res_nome_cliente = request.POST['nome-cliente'],
            res_telefone_cliente = telefone,
            res_data_atendimento = data_formatada,
            res_periodo_atendimento = request.POST['periodo-atendimento'],
            res_especialista = request.POST['nome-especialista'],
            res_servicos = servicos
        )

        novo_agendamento.save()
        messages.success(request, 'Agendamento realizado com sucesso.', extra_tags='alert-success')
        return redirect('cadastrarAgendamento')
    
    return render(request, 'minha-conta/agenda/cadastro.html')

def excluirAgendamento(request, id):
    if request.method == "POST":
        instance = Reserva.objects.get(id=id)
        instance.delete()
        return redirect('agendamentosCadastrados')

# Função que retorna o dia da semana a partir
# de uma string no formato: yyyy-mm-dd
def diaDaSemana(data):

    DIAS = [
        'Segunda-feira',
        'Terça-feira',
        'Quarta-feira',
        'Quinta-Feira',
        'Sexta-feira',
        'Sábado',
        'Domingo'
    ]

    data = data.replace('-', ' ')
    ano = int(data.split()[0])
    mes = int(data.split()[1])
    dia = int(data.split()[2])

    data = date(year=ano, month=mes, day=dia)
    indice_da_semana = data.weekday()
    dia_da_semana = DIAS[indice_da_semana]

    return dia_da_semana

# Função para listar apenas os períodos livres
def periodosDisponiveis(request):
    sem_periodo_disponivel = False
    servicos_cadastrados = Servico.objects.all()
    
    periodos_chiquinho = {
            '9-10' : 'Das 9hr as 10hrs',
            '10-11' : 'Das 10hr as 11hrs',
            '13-14' : 'Das 13hr as 14hrs',
            '14-15' : 'Das 14hr as 15hrs',
            '15-16' : 'Das 15hr as 16hrs',
            '16-17' : 'Das 16hr as 17hrs',
            '17-18' : 'Das 17hr as 18hrs',
            '18-19' : 'Das 18hr as 19hrs',
            '19-20' : 'Das 19hr as 20hrs',
    }

    periodos_sandrinho = {
            '9-10' : 'Das 9hr as 10hrs',
            '10-11' : 'Das 10hr as 11hrs',
            '13-14' : 'Das 13hr as 14hrs',
            '14-15' : 'Das 14hr as 15hrs',
            '15-16' : 'Das 15hr as 16hrs',
            '16-17' : 'Das 16hr as 17hrs',
            '17-18' : 'Das 17hr as 18hrs',
            '18-19' : 'Das 18hr as 19hrs',
            '19-20' : 'Das 19hr as 20hrs',
    }

    if request.method == "POST":
        # Validando se a data não foi enviada vazia
        data = request.POST['dia-atendimento']
        if data == '':
            messages.success(request, 'Informe uma data.', extra_tags='alert-danger')
            return redirect('cadastrarAgendamento')

        # Pegando a data enviada pelo usuário e desmembrando
        data = data.replace('-', ' ')
        ano = int(data.split()[0])
        mes = int(data.split()[1])
        dia = int(data.split()[2])
        data_enviada = '{dia}/{mes}/{ano}'.format(dia=str(dia), mes=str(mes), ano=str(ano))
        data_enviada_label = data_enviada


        # Pegando a data atual do computador e 
        # verificando se a data solicitada não é retroativa
        data_local = datetime.date.today()
        dia_local = data_local.strftime("%d")
        mes_local = data_local.strftime("%m")
        ano_local = data_local.strftime("%y")
        data_local = '{dia}/{mes}/{ano}20'.format(dia=dia_local, mes=mes_local, ano=ano_local)

        # Convertendo a data enviada em timestamp
        data_enviada = datetime.datetime.strptime(data_enviada,  "%d/%m/%Y")
        timestamp_data_enviada = datetime.datetime.timestamp(data_enviada)

        # Convertendo a data local em timestamp
        data_local = datetime.datetime.strptime(data_local,  "%d/%m/%Y")
        timestamp_data_local = datetime.datetime.timestamp(data_local)

        if timestamp_data_enviada < timestamp_data_local:
            messages.success(request, 'A data informada é inválida.', extra_tags='alert-danger')
            return redirect('cadastrarAgendamento')

        # Consultando todos os registros da data enviada    
        reservas = Reserva.objects.filter(res_data_atendimento=datetime.date(ano, mes, dia))

        # Se houver algum resultado é verificado qual o 
        # período está reservado por especialista e o período
        # reservado é removido do dicionário de períodos
        if len(reservas.values()) > 0:
            especialista_indisponivel = ''
            for index in range(len(reservas.values())):
                nome_especialista = reservas.values()[index]['res_especialista']
                periodo_reservado = reservas.values()[index]['res_periodo_atendimento']

                if nome_especialista == 'Chiquinho Oliveira':
                    periodos_chiquinho.pop(periodo_reservado)
                else:
                    periodos_sandrinho.pop(periodo_reservado)

                if len(periodos_chiquinho) == 0:
                    sem_periodo_disponivel = True
                    especialista_indisponivel = 'Chiquinho Oliveira'

                if len(periodos_sandrinho) == 0:
                    sem_periodo_disponivel = True
                    especialista_indisponivel = 'Sandrinho Santos'
                    
            
            contexto = {
                'periodos_chiquinho' : periodos_chiquinho,
                'periodos_sandrinho' : periodos_sandrinho,
                'sem_periodo_disponivel' : sem_periodo_disponivel,
                'especialista_indisponivel' : especialista_indisponivel,
                'data_selecionada' : data_enviada_label,
                'servicos_cadastrados' : servicos_cadastrados
            }
            return render(request, 'minha-conta/agenda/cadastro.html', contexto)
        
        contexto = {
            'periodos_chiquinho' : periodos_chiquinho,
            'periodos_sandrinho' : periodos_sandrinho,
            'sem_periodo_disponivel' : sem_periodo_disponivel,
            'data_selecionada' : data_enviada_label,
            'servicos_cadastrados' : servicos_cadastrados
        }
        return render(request, 'minha-conta/agenda/cadastro.html', contexto)

    return render(request, 'minha-conta/agenda/cadastro.html')

# <QueryDict: {
#     'csrfmiddlewaretoken': ['IrGFgAU5EJgh0au9foBnZibGGe3ZtbjfyPe93qh5F6Hhc3HY15OaauqdfgIbt6F8'], 
#     'nome-especialista': ['Chiquinho Oliveira'],
#     'data_selecionada': ['20/5/2020'], 
#     'nome-cliente': ['Lenildo'], 
#     'telefone-cliente': ['11'], 
#     'periodo-atendimento': ['9-10'], 
#     'servicos-selecionados': ['Corte na Tesoura', 'Corte', 'Barba', 'Corte Dimil']}>
