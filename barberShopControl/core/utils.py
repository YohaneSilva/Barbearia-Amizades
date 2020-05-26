from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import FileResponse, HttpResponse

import io
import smtplib
import hashlib
import random
from email.mime.text import MIMEText
from datetime import date, datetime
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from .models import *

class Avaliacao:
    def grauAvaliacao():
        pass

class Relatorio:
    def agendamentosDoMes():
        dia, mes, ano = Data.desmembrarData(Data.dataDoComputador('/'))
        reservas_mes = Reserva.objects.filter(res_data_atendimento__year=ano, res_data_atendimento__month=mes)
        
        return reservas_mes

    def agendamentosCancelados():
        return Reserva.objects.filter(res_status='Cancelado')
    
    def agendamentosPendentes():
        return Reserva.objects.filter(res_status='Pendente')
    
    def agendamentosFinalizados():
        return Reserva.objects.filter(res_status='Finalizado')

    def agendamentosAtivos():
        return Reserva.objects.filter(res_status='Ativo')
    
    def agendamentosEspecialista(especialista):
        return  Reserva.objects.filter(res_especialista=especialista)
    
    def agendamentosPorServico(servico):
        return  Reserva.objects.filter(res_servicos__icontains=servico)

    # Totalizadores
    def totalAgendamentos():
        total = 0
        resultado = Reserva.objects.all()
        
        for index in range(len(resultado)):
            total += 1
        
        return total

    def totalAgendamentosDoAno():
        total = 0
        dia, mes, ano = Data.desmembrarData(Data.dataDoComputador('/'))
        reservas_mes = Reserva.objects.filter(res_data_atendimento__year=ano)
        
        for index in range(len(reservas_mes)):
            total += 1
        
        return total

    def totalAgendamentosDoMes():
        total = 0
        dia, mes, ano = Data.desmembrarData(Data.dataDoComputador('/'))
        reservas_mes = Reserva.objects.filter(res_data_atendimento__year=ano, res_data_atendimento__month=mes)
        
        for index in range(len(reservas_mes)):
            total += 1
        
        return total
    
    def totalAgendamentosCancelados():
        total = 0
        resultado = Reserva.objects.filter(res_status='Cancelado')

        for index in range(len(resultado)):
            total += 1
        
        return total
    
    def totalAgendamentosPendentes():
        total = 0
        resultado = Reserva.objects.filter(res_status='Pendente')
        
        for index in range(len(resultado)):
            total += 1
        
        return total
    
    def totalAgendamentosFinalizados():
        total = 0
        resultado = Reserva.objects.filter(res_status='Finalizado')

        for index in range(len(resultado)):
            total += 1
        
        return total

    def totalAgendamentosAtivos():
        total = 0
        resultado = Reserva.objects.filter(res_status='Ativo')

        for index in range(len(resultado)):
            total += 1
        
        return total

    def totalAgendamentosChiquinho():
        total = 0
        resultado = Reserva.objects.filter(res_especialista='Chiquinho Oliveira')

        for index in range(len(resultado)):
            total += 1
        
        return total

    def totalAgendamentosSandrinho():
        total = 0
        resultado = Reserva.objects.filter(res_especialista='Sandrinho Santos')

        for index in range(len(resultado)):
            total += 1
        
        return total
    
    def totalAgendamentoPorServico():
        servicos = Servico.objects.all()
        total = {}
        contador = 0
        for servico in servicos:
            servico = str(servico)
            total[servico] = ''
            reservas = Reserva.objects.filter(res_servicos__icontains=servico)
            contador = len(reservas)
            total[servico] = str(contador)

        return total

class Telefone:
    def quantidadeCaracteres(telefone):
        if len(telefone) > 11:
            return True
    
    def validarCampo(request):
        telefone = request.POST['telefone-cliente']

        if Telefone.quantidadeCaracteres(telefone):
            messages.success(request, 'Os dados informados estão incorretos.', extra_tags='alert-danger')
            return True
        else:
            return False

class Periodo:
    def periodos():
        periodos_disponiveis = {
            '9-10' : 'Das 9hr as 10hrs',
            '10-11' : 'Das 10hr as 11hrs',
            '13-14' : 'Das 13hr as 14hrs',
            '14-15' : 'Das 14hr as 15hrs',
            '15-16' : 'Das 15hr as 16hrs',
            '16-17' : 'Das 16hr as 17hrs',
            '17-18' : 'Das 17hr as 18hrs',
            '18-19' : 'Das 18hr as 19hrs',
            '19-20' : 'Das 19hr as 20hrs'
        }

        return periodos_disponiveis

    # Listar apenas os períodos livres
    # dentro do módulo administrativo
    def periodosDisponiveis(request):
        # Consultando todos os registros da data enviada
        dia, mes, ano = Data.desmembrarData(request.POST['dia-atendimento'])
        reservas = Reserva.objects.filter(res_data_atendimento__year=ano, res_data_atendimento__month=mes, res_data_atendimento__day=dia)
        sem_periodo_disponivel = False
        periodos_chiquinho = Periodo.periodos()
        periodos_sandrinho = Periodo.periodos()
        data_enviada_formatada = Data.formatarDataComMes(request.POST['dia-atendimento'],' de ')
        data_enviada = Data.formatarData(request.POST['dia-atendimento'],'/')
        servicos_cadastrados = Servicos.retornarTodosServicos()

        # Se houver algum resultado é verificado qual o 
        # período está reservado por especialista e o período
        # reservado é removido do dicionário de períodos
        if len(reservas.values()) <= 0:
            contexto = {
                'status ' : False,
                'periodos_chiquinho' : periodos_chiquinho,
                'periodos_sandrinho' : periodos_sandrinho,
                'sem_periodo_disponivel' : sem_periodo_disponivel,
                'data_enviada_formatada' : data_enviada_formatada,
                'data_enviada' : data_enviada,
                'servicos_cadastrados' : servicos_cadastrados
            }
            return contexto

        else:
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
                'data_enviada_formatada' : data_enviada_formatada,
                'data_enviada' : data_enviada,
                'servicos_cadastrados' : servicos_cadastrados
            }
            return contexto

class Login:
    def verificarUsuarioLogado(request):
        try:
            if request.session['logado']:
                return request.session['nome_usuario_logado']
            else:
                return False
        except KeyError:
            Sessao.criarVariaveisSessao(request)
            Login.verificarUsuarioLogado(request)

    def validarLogin(request):
        usuario = request.POST['usuario']
        senha = request.POST['senha']
        resultado_busca = Usuario.objects.filter(us_usuario=usuario, us_senha=senha)

        if len(resultado_busca.values()) > 0:
            for nome in resultado_busca:
                request.session['usuario_logado'] = usuario
                request.session['nome_usuario_logado'] = str(nome)
                request.session['logado'] = True
            return True

        else:
            messages.success(request, 'E-mail ou senha inválido.', extra_tags='alert-danger')
            return False

    def deslogar(request):
        request.session['usuario_logado'] = ''
        request.session['nome_usuario_logado'] = ''
        request.session['logado'] = False

class Senha:
    def gerarSenhaRandomica():
        caracters = '0123456789abcdefghijlmnopqrstuwvxzABCDEFGHIJKLMNOPQRSTUVXWYZ'
        senha = ''
        for char in range(10):
                senha += random.choice(caracters)
        return senha

class Sessao:
    def criarVariaveisSessao(request):
        request.session['usuario_logado'] = ''
        request.session['nome_usuario_logado'] = ''
        request.session['logado'] = False

class Data:
    def desmembrarData(data):
        if '-' in data:
            data = data.replace('-', ' ')
            ano = data.split()[0]
            mes = data.split()[1]
            dia = data.split()[2]
            return dia, mes, ano

        elif '/' in data:
            data = data.replace('/', ' ')
            ano = data.split()[2]
            mes = data.split()[1]
            dia = data.split()[0]
            return dia, mes, ano

    def dataRetroativa(request):
        data = Data.formatarData(request.POST['dia-atendimento'], '/')
        # Convertendo a data enviada em timestamp
        timestamp_data_enviada = datetime.strptime(data,  "%d/%m/%Y")
        timestamp_data_enviada = datetime.timestamp(timestamp_data_enviada)

        # Convertendo a data do computador em timestamp
        data_computador = Data.dataDoComputador('/')
        data_computador = datetime.strptime(data_computador,  "%d/%m/%Y")
        timestamp_data_computador = datetime.timestamp(data_computador)

        if timestamp_data_enviada < timestamp_data_computador:
            messages.success(request, 'A data informada é inválida.', extra_tags='alert-danger')
            return True

    def dataRetroativaDoBanco(data):
        data = Data.formatarData(data, '/')
        # Convertendo a data enviada em timestamp
        timestamp_data_enviada = datetime.strptime(data,  "%d/%m/%Y")
        timestamp_data_enviada = datetime.timestamp(timestamp_data_enviada)

        # Convertendo a data do computador em timestamp
        data_computador = Data.dataDoComputador('/')
        data_computador = datetime.strptime(data_computador,  "%d/%m/%Y")
        timestamp_data_computador = datetime.timestamp(data_computador)

        if timestamp_data_enviada < timestamp_data_computador:
            return True

    def dataVazia(request):
        data = request.POST['dia-atendimento']
        if data == '':
            messages.success(request, 'Informe uma data.', extra_tags='alert-danger')
            return True
    
    def formatarData(data, separador):
        if type(data) == str:
            if '-' in data:
                data = data.replace('-', ' ')
                ano = data.split()[0]
                mes = data.split()[1]
                dia = data.split()[2]
                data = '{dia}{separador}{mes}{separador}{ano}'.format(dia=dia, mes=mes, ano=ano, separador=separador)
                return data

            elif '/' in data:
                data = data.replace('/', ' ')
                ano = data.split()[2]
                mes = data.split()[1]
                dia = data.split()[0]
                data = '{dia}{separador}{mes}{separador}{ano}'.format(dia=dia, mes=mes, ano=ano, separador=separador)
                return data
        else:
            dia = data.strftime("%d")
            mes = data.strftime("%m")
            ano = data.strftime("%Y")
            data = '{dia}{separador}{mes}{separador}{ano}'.format(dia=dia, mes=mes, ano=ano, separador=separador)
            return data

    def formatarDataComMes(data, separador):
        if type(data) == str:
            if '-' in data:
                data = data.replace('-', ' ')
                ano = data.split()[0]
                mes = data.split()[1]
                dia = data.split()[2]
                data = '{dia}{separador}{mes}{separador}{ano}'.format(dia=dia, mes=Data.mesDoAno(mes), ano=ano, separador=separador)
                return data

            elif '/' in data:
                data = data.replace('/', ' ')
                ano = data.split()[2]
                mes = data.split()[1]
                dia = data.split()[0]
                data = '{dia}{separador}{mes}{separador}{ano}'.format(dia=dia, mes=Data.mesDoAno(mes), ano=ano, separador=separador)
                return data
        else:
            dia = data.strftime("%d")
            mes = data.strftime("%m")
            ano = data.strftime("%Y")
            data = '{dia}{separador}{mes}{separador}{ano}'.format(dia=dia, mes=Data.mesDoAno(mes), ano=ano, separador=separador)
            return data

    def dataDoComputador(separador):
        data = date.today()
        dia = data.strftime("%d")
        mes = data.strftime("%m")
        ano = data.strftime("%Y")
        data = '{dia}{separador}{mes}{separador}{ano}'.format(dia=dia, mes=mes, ano=ano, separador=separador)

        return data

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

    def mesDoAno(dia):
        meses_ano = {
            '01': 'Janeiro',
            '02': 'Fevereiro',
            '03': 'Março',
            '04': 'Abril',
            '05': 'Maio',
            '06': 'Junho',
            '07': 'Julho',
            '08': 'Agosto',
            '09': 'Setembro',
            '10': 'Outubro',
            '11': 'Novembro',
            '12': 'Dezembro'
        }

        return meses_ano[dia]

class Conta:
    def validarRecuperacaoDeSenha(request):
        email = request.POST['email']
        usuario = request.POST['usuario']
        resultado_busca = Usuario.objects.filter(us_email=email, us_usuario=usuario)

        if len(resultado_busca.values()) > 0:
            contexto = {
                'status' : True,
                'resultado_busca' : resultado_busca,
                'email' : email,
                'usuario' : usuario,
                'especialista' : resultado_busca.values('us_nome')[0]['us_nome']
            }
        else:
            contexto = {
                'status' : False,
            }
            messages.success(request, 'Usuário ou e-mail inválido.', extra_tags='alert-danger')
        return contexto

class Agendamento:
    def finalizarAgendamento(request):
        nome_cliente  = request.POST['nome-cliente']
        email_destino = request.POST['email-cliente']
        data_agendada = request.POST['data-agendada']

        Email.finalizarAtendimento(email_destino, nome_cliente, data_agendada)
        Reserva.objects.filter(id=request.POST['id-registro']).update(res_observacao_especialista=request.POST['observacao-atendimento'], res_status='Finalizado')

    def cancelarAgendamento(request):
        Email.cancelarAgendamento(request, request.POST['id-registro'])
        Reserva.objects.filter(id=request.POST['id-registro']).update(res_observacao_especialista=request.POST['observacao-atendimento'],res_status='Cancelado')
        messages.success(request, 'Agendamento cancelado.', extra_tags='alert-success')

    def agendamentoPendente():
        agendamentos_cadastrados = Reserva.objects.all()
        
        for valor in agendamentos_cadastrados:
            data_atendimento = getattr(valor, 'res_data_atendimento')
            status = getattr(valor, 'res_status')
            
            if Data.dataRetroativaDoBanco(data_atendimento) and status == 'Ativo':
                Reserva.objects.all().update(res_status='Pendente')

    def retornarTodosAgendamentos():
        return Reserva.objects.all()
    
    def agendamentoUnico(request):
        dia, mes, ano = Data.desmembrarData(request.POST['data-enviada'])
        data_formatada = Data.formatarDataComMes(request.POST['data-enviada'], ' de ')
        reservas = Reserva.objects.filter(res_data_atendimento__year=ano, res_data_atendimento__month=mes, res_data_atendimento__day=dia)

        if len(reservas.values()) > 0:
            for index in range(len(reservas.values())):
                nome_cliente = reservas.values()[index]['res_nome_cliente']

                if nome_cliente == request.POST['nome-cliente']:
                    messages.success(request, 'Você já possui um agendamento na dia {data} selecionada.'.format(data=data_formatada), extra_tags='alert-danger')
                    return True

class Servicos:
    def retornarTodosServicos():
        return Servico.objects.all()
    
    def retornarListaServicos():
        servicos_cadastrados = Servico.objects.all()
        servicos = []
        contador = 0
        for servico in servicos_cadastrados:
            servico = str(servico)
            servicos.append(servico)

        return servicos

class Email:
    def finalizarAtendimento(email_destino, nome_cliente, data_agendada, codigo_verificacao):
        assunto = 'Finalizar Atendimento | Barbearia Amizades S & D'
        titulo = """\
                <strong>Atendimento Finalizado</strong>
            """
        mensagem = """\
            Olá <strong>{cliente}.</strong> 
            <br><br>
            O agendamento do dia <strong>{data}</strong> foi encerrado com sucesso!
            <br><br>
            Ficaríamos felizes se você avaliasse nosso atendimento. Muito simples e rápido. Basta <strong><a href="http://127.0.0.1:8000/{codigo}/avaliacao"> clicar aqui</a></strong>.            

            <br><br>
            Agradecemos a preferência!
            """.format(cliente=nome_cliente, data=data_agendada, codigo=codigo_verificacao)
        
        Email.enviarEmail(assunto, Email.corpoEmail(titulo, mensagem), email_destino)
        
    def recuperarSenha(request, email_destino, especialista, senha):
        data = Data.dataDoComputador(' de ')
        assunto = 'Recuperar Senha | Barbearia Amizades S & D'
        titulo = """\
                <strong>Nova Senha</strong>
            """
        mensagem = """\
            Olá <strong>{especialista}.</strong>
            <br><br>
            A alteração de senha solicitada no dia <strong>{data}</strong>, foi um <strong>sucesso!</strong>
            <br><br>
            Sua nova senha é: <strong>{senha}</strong>
            """.format(especialista=especialista, data=data, senha=senha)
        
        Email.enviarEmail(assunto, Email.corpoEmail(titulo, mensagem), email_destino)

        messages.success(request, 'Nova senha enviada por e-mail.', extra_tags='alert-success')
    
    def novoAgendamento(request, codigo_verificacao):
        periodo_reservado = Periodo.periodos()
        periodo_reservado = periodo_reservado[request.POST['periodo-atendimento']].lower()

        data_agendada = request.POST['data-enviada-por-email']
        nome_cliente = request.POST['nome-cliente']
        nome_especialista = request.POST['nome-especialista']
        email_destino = request.POST['email-cliente']
        servicos = ', '.join(request.POST.getlist('servicos-selecionados'))
        assunto = 'Realizar Agendamento | Barbearia Amizades S & D'
        titulo = """\
                <strong>Agendamento Realizado</strong>
            """
        mensagem = """\
             Olá <strong>{cliente}.</strong> 
            <br><br>
            O agendamento do dia <strong>{data}</strong>, no período <strong>{periodo}</strong> com o especialista <strong>{especialista}</strong>, foi efetuado com sucesso!
            <br><br>
            Os serviços reservados foram: <strong>{servico}</strong>.
            <br><br>
            Para cancelar o agendamento <a href="http://127.0.0.1:8000/{codigo}">clique aqui</a>
            """.format(cliente=nome_cliente, data=data_agendada, especialista=nome_especialista, periodo=periodo_reservado, servico=servicos, codigo=codigo_verificacao)
        
        Email.enviarEmail(assunto, Email.corpoEmail(titulo, mensagem), email_destino)

    def cancelarAgendamento(request, id_registro):
        resultado_busca = Reserva.objects.filter(id=id_registro)
        data_agendada = Data.formatarDataComMes(resultado_busca.values('res_data_atendimento')[0]['res_data_atendimento'], ' de ')

        nome_cliente = resultado_busca.values('res_nome_cliente')[0]['res_nome_cliente']
        nome_especialista = resultado_busca.values('res_especialista')[0]['res_especialista']
        email_destino = resultado_busca.values('res_email_cliente')[0]['res_email_cliente']
        assunto = 'Cancelar Agendamento | Barbearia Amizades S & D'
        titulo = """\
                <strong>Agendamento Cancelado</strong>
            """
        mensagem = """\
            Olá <strong>{cliente}.</strong> <br><br> O agendamento para o dia <strong>{data}</strong>, com o especialista <strong>{especialista}</strong>, foi cancelado com sucesso.
            """.format(cliente=nome_cliente, data=data_agendada, especialista=nome_especialista)
        
        Email.enviarEmail(assunto, Email.corpoEmail(titulo, mensagem), email_destino)

    def enviarEmail(assunto, mensagem, email_destino):
        # conexão com os servidores do google
        smtp_ssl_host = 'smtp.gmail.com'
        smtp_ssl_port = 465
        # username ou email para logar no servidor
        username = 'barbeariaamizades@gmail.com'
        password = 'amizades.1234'
        from_addr = 'barbeariaamizades@gmail.com'
        to_addrs = [email_destino]
        # a biblioteca email possuí vários templates
        # para diferentes formatos de mensagem
        # neste caso usaremos MIMEText para enviar
        # somente texto
        message = MIMEText(mensagem, 'html')
        message['subject'] = assunto
        message['from'] = from_addr
        message['to'] = ', '.join(to_addrs)
        # conectaremos de forma segura usando SSL
        server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
        # para interagir com um servidor externo precisaremos
        # fazer login nele
        server.login(username, password)
        server.sendmail(from_addr, to_addrs, message.as_string())
        server.quit()

    def corpoEmail(titulo, mensagem):
        corpo = """\
                    <body class="clean-body" style="margin: 0; padding: 0; -webkit-text-size-adjust: 100%; background-color: #f8f8f9;">
                        <!--[if IE]><div class="ie-browser"><![endif]-->
                        <table bgcolor="#f8f8f9" cellpadding="0" cellspacing="0" class="nl-container" role="presentation" style="table-layout: fixed; vertical-align: top; min-width: 320px; Margin: 0 auto; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #f8f8f9; width: 100%;" valign="top" width="100%">
                            <tbody>
                                <tr style="vertical-align: top;" valign="top">
                                    <td style="word-break: break-word; vertical-align: top;" valign="top">
                                        <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" style="background-color:#f8f8f9"><![endif]-->
                                        <div style="background-color:#FDCB8D;">
                                            <div class="block-grid" style="Margin: 0 auto; min-width: 320px; max-width: 640px; overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; background-color: #FDCB8D;">
                                                <div style="border-collapse: collapse;display: table;width: 100%;background-color:#FDCB8D;">
                                                    <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#FDCB8D;"><tr><td align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:640px"><tr class="layout-full-width" style="background-color:#FDCB8D"><![endif]-->
                                                    <!--[if (mso)|(IE)]><td align="center" width="640" style="background-color:#FDCB8D;width:640px; border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent;" valign="top"><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 0px; padding-left: 0px; padding-top:0px; padding-bottom:0px;"><![endif]-->
                                                    <div class="col num12" style="min-width: 320px; max-width: 640px; display: table-cell; vertical-align: top; width: 640px;">
                                                        <div style="width:100% !important;">
                                                            <!--[if (!mso)&(!IE)]><!-->
                                                            <div style="border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; border-right:0px solid transparent; padding-top:0px; padding-bottom:0px; padding-right: 0px; padding-left: 0px;">
                                                                <!--<![endif]-->
                                                                <table border="0" cellpadding="0" cellspacing="0" class="divider" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top" width="100%">
                                                                    <tbody>
                                                                        <tr style="vertical-align: top;" valign="top">
                                                                            <td class="divider_inner" style="word-break: break-word; vertical-align: top; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px;" valign="top">
                                                                                <table align="center" border="0" cellpadding="0" cellspacing="0" class="divider_content" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-top: 4px solid #FDCB8D; width: 100%;" valign="top" width="100%">
                                                                                    <tbody>
                                                                                        <tr style="vertical-align: top;" valign="top">
                                                                                            <td style="word-break: break-word; vertical-align: top; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top"><span></span></td>
                                                                                        </tr>
                                                                                    </tbody>
                                                                                </table>
                                                                            </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            <!--[if (!mso)&(!IE)]><!-->
                                                            </div>
                                                        <!--<![endif]-->
                                                        </div>
                                                    </div>
                                                <!--[if (mso)|(IE)]></td></tr></table><![endif]-->
                                                <!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]-->
                                                </div>
                                            </div>
                                        </div>
                                        <div style="background-color:transparent;">
                                            <div class="block-grid" style="Margin: 0 auto; min-width: 320px; max-width: 640px; overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; background-color: #f8f8f9;">
                                                <div style="border-collapse: collapse;display: table;width: 100%;background-color:#f8f8f9;">
                                                    <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:transparent;"><tr><td align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:640px"><tr class="layout-full-width" style="background-color:#f8f8f9"><![endif]-->
                                                    <!--[if (mso)|(IE)]><td align="center" width="640" style="background-color:#f8f8f9;width:640px; border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent;" valign="top"><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 0px; padding-left: 0px; padding-top:5px; padding-bottom:5px;"><![endif]-->
                                                    <div class="col num12" style="min-width: 320px; max-width: 640px; display: table-cell; vertical-align: top; width: 640px;">
                                                        <div style="width:100% !important;">
                                                            <!--[if (!mso)&(!IE)]><!-->
                                                            <div style="border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; border-right:0px solid transparent; padding-top:5px; padding-bottom:5px; padding-right: 0px; padding-left: 0px;">
                                                                <!--<![endif]-->
                                                                <table border="0" cellpadding="0" cellspacing="0" class="divider" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top" width="100%">
                                                                    <tbody>
                                                                        <tr style="vertical-align: top;" valign="top">
                                                                            <td class="divider_inner" style="word-break: break-word; vertical-align: top; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; padding-top: 20px; padding-right: 20px; padding-bottom: 20px; padding-left: 20px;" valign="top">
                                                                                <table align="center" border="0" cellpadding="0" cellspacing="0" class="divider_content" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-top: 0px solid #BBBBBB; width: 100%;" valign="top" width="100%">
                                                                                    <tbody>
                                                                                        <tr style="vertical-align: top;" valign="top">
                                                                                            <td style="word-break: break-word; vertical-align: top; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top"><span></span></td>
                                                                                        </tr>
                                                                                    </tbody>
                                                                                </table>
                                                                            </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            <!--[if (!mso)&(!IE)]><!-->
                                                            </div>
                                                        <!--<![endif]-->
                                                        </div>
                                                    </div>
                                                <!--[if (mso)|(IE)]></td></tr></table><![endif]-->
                                                <!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]-->
                                                </div>
                                            </div>
                                        </div>
                                        <div style="background-color:transparent;">
                                            <div class="block-grid" style="Margin: 0 auto; min-width: 320px; max-width: 640px; overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; background-image: url(https://i1.wp.com/annettejohansen.no/wp-content/uploads/2017/04/white-background-2.jpg?fit=1200%2C703);">
                                                <div style="border-collapse: collapse;display: table;width: 100%;background-image: url(https://i1.wp.com/annettejohansen.no/wp-content/uploads/2017/04/white-background-2.jpg?fit=1200%2C703);">
                                                    <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:transparent;"><tr><td align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:640px"><tr class="layout-full-width" style="background-image: url(https://i1.wp.com/annettejohansen.no/wp-content/uploads/2017/04/white-background-2.jpg?fit=1200%2C703);"><![endif]-->
                                                    <!--[if (mso)|(IE)]><td align="center" width="640" style="background-image: url(https://i1.wp.com/annettejohansen.no/wp-content/uploads/2017/04/white-background-2.jpg?fit=1200%2C703);;width:640px; border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent;" valign="top"><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 0px; padding-left: 0px; padding-top:0px; padding-bottom:0px;"><![endif]-->
                                                    <div class="col num12" style="min-width: 320px; max-width: 640px; display: table-cell; vertical-align: top; width: 640px;">
                                                        <div style="width:100% !important;">
                                                            <!--[if (!mso)&(!IE)]><!-->
                                                            <div style="border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; border-right:0px solid transparent; padding-top:0px; padding-bottom:0px; padding-right: 0px; padding-left: 0px;">
                                                                <!--<![endif]-->
                                                                <table border="0" cellpadding="0" cellspacing="0" class="divider" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top" width="100%">
                                                                    <tbody>
                                                                        <tr style="vertical-align: top;" valign="top">
                                                                            <td class="divider_inner" style="word-break: break-word; vertical-align: top; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; padding-top: 60px; padding-right: 0px; padding-bottom: 12px; padding-left: 0px;" valign="top">
                                                                                <table align="center" border="0" cellpadding="0" cellspacing="0" class="divider_content" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-top: 0px solid #BBBBBB; width: 100%;" valign="top" width="100%">
                                                                                    <tbody>
                                                                                        <tr style="vertical-align: top;" valign="top">
                                                                                            <td style="word-break: break-word; vertical-align: top; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top"><span></span></td>
                                                                                        </tr>
                                                                                    </tbody>
                                                                                </table>
                                                                            </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                                <div align="center" class="img-container center fixedwidth" style="padding-right: 40px;padding-left: 40px;">
                                                                <!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr style="line-height:0px"><td style="padding-right: 40px;padding-left: 40px;" align="center"><![endif]--><img align="center" alt="Logo Barbearia Amizades S & D" border="0" class="center fixedwidth" src="https://i.ibb.co/4dRPWtz/logo.png" style="text-decoration: none; -ms-interpolation-mode: bicubic; border: 0; height: auto; width: 100%; max-width: 352px; display: block;" title="Logo Barbearia Amizades S & D" width="352"/>
                                                                <!--[if mso]></td></tr></table><![endif]-->
                                                                </div>
                                                                <table border="0" cellpadding="0" cellspacing="0" class="divider" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top" width="100%">
                                                                    <tbody>
                                                                        <tr style="vertical-align: top;" valign="top">
                                                                            <td class="divider_inner" style="word-break: break-word; vertical-align: top; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; padding-top: 50px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px;" valign="top">
                                                                                <table align="center" border="0" cellpadding="0" cellspacing="0" class="divider_content" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-top: 0px solid #BBBBBB; width: 100%;" valign="top" width="100%">
                                                                                    <tbody>
                                                                                        <tr style="vertical-align: top;" valign="top">
                                                                                            <td style="word-break: break-word; vertical-align: top; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top"><span></span></td>
                                                                                        </tr>
                                                                                    </tbody>
                                                                                </table>
                                                                            </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                                <!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 40px; padding-left: 40px; padding-top: 10px; padding-bottom: 10px; font-family: Tahoma, sans-serif"><![endif]-->
                                                                <div style="color:#555555;font-family:Montserrat, Trebuchet MS, Lucida Grande, Lucida Sans Unicode, Lucida Sans, Tahoma, sans-serif;line-height:1.2;padding-top:10px;padding-right:40px;padding-bottom:10px;padding-left:40px;">
                                                                    <div style="line-height: 1.2; font-size: 12px; color: #555555; font-family: Montserrat, Trebuchet MS, Lucida Grande, Lucida Sans Unicode, Lucida Sans, Tahoma, sans-serif; mso-line-height-alt: 14px;">
                                                                        <p style="font-size: 30px; line-height: 1.2; text-align: center; word-break: break-word; mso-line-height-alt: 36px; margin: 0;">
                                                                            <span style="font-size: 30px; color: #2b303a;">
                                                                                {titulo}
                                                                            </span>
                                                                        </p>
                                                                    </div>
                                                                </div>
                                                                <!--[if mso]></td></tr></table><![endif]-->
                                                                <!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 40px; padding-left: 40px; padding-top: 10px; padding-bottom: 10px; font-family: Tahoma, sans-serif"><![endif]-->
                                                                <div style="color:#555555;font-family:Montserrat, Trebuchet MS, Lucida Grande, Lucida Sans Unicode, Lucida Sans, Tahoma, sans-serif;line-height:1.5;padding-top:10px;padding-right:40px;padding-bottom:10px;padding-left:40px;">
                                                                    <div style="line-height: 1.5; font-size: 12px; font-family: Montserrat, Trebuchet MS, Lucida Grande, Lucida Sans Unicode, Lucida Sans, Tahoma, sans-serif; color: #555555; mso-line-height-alt: 18px;">
                                                                        <p style="font-size: 15px; line-height: 1.5; text-align: left; word-break: break-word; font-family: inherit; mso-line-height-alt: 23px; margin: 0;">
                                                                            <span style="color: #808389; font-size: 15px;">
                                                                                {mensagem}
                                                                            </span>
                                                                        </p>
                                                                    </div>
                                                                </div>
                                                                <!--[if mso]></td></tr></table><![endif]-->
                                                                <table border="0" cellpadding="0" cellspacing="0" class="divider" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top" width="100%">
                                                                    <tbody>
                                                                        <tr style="vertical-align: top;" valign="top">
                                                                            <td class="divider_inner" style="word-break: break-word; vertical-align: top; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; padding-top: 60px; padding-right: 0px; padding-bottom: 12px; padding-left: 0px;" valign="top">
                                                                                <table align="center" border="0" cellpadding="0" cellspacing="0" class="divider_content" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-top: 0px solid #BBBBBB; width: 100%;" valign="top" width="100%">
                                                                                    <tbody>
                                                                                        <tr style="vertical-align: top;" valign="top">
                                                                                            <td style="word-break: break-word; vertical-align: top; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top"><span></span></td>
                                                                                        </tr>
                                                                                    </tbody>
                                                                                </table>
                                                                            </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            <!--[if (!mso)&(!IE)]><!-->
                                                            </div>
                                                        <!--<![endif]-->
                                                        </div>
                                                    </div>
                                                    <!--[if (mso)|(IE)]></td></tr></table><![endif]-->
                                                <!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]-->
                                                </div>
                                            </div>
                                        </div>
                                        <div style="background-color:transparent;">
                                            <div class="block-grid" style="Margin: 0 auto; min-width: 320px; max-width: 640px; overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; background-color: #f8f8f9;">
                                                <div style="border-collapse: collapse;display: table;width: 100%;background-color:#f8f8f9;">
                                                <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:transparent;"><tr><td align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:640px"><tr class="layout-full-width" style="background-color:#f8f8f9"><![endif]-->
                                                    <!--[if (mso)|(IE)]><td align="center" width="640" style="background-color:#f8f8f9;width:640px; border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent;" valign="top"><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 0px; padding-left: 0px; padding-top:5px; padding-bottom:5px;"><![endif]-->
                                                    <div class="col num12" style="min-width: 320px; max-width: 640px; display: table-cell; vertical-align: top; width: 640px;">
                                                        <div style="width:100% !important;">
                                                        <!--[if (!mso)&(!IE)]><!-->
                                                            <div style="border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; border-right:0px solid transparent; padding-top:5px; padding-bottom:5px; padding-right: 0px; padding-left: 0px;">
                                                            <!--<![endif]-->
                                                                <table border="0" cellpadding="0" cellspacing="0" class="divider" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top" width="100%">
                                                                    <tbody>
                                                                        <tr style="vertical-align: top;" valign="top">
                                                                            <td class="divider_inner" style="word-break: break-word; vertical-align: top; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; padding-top: 20px; padding-right: 20px; padding-bottom: 20px; padding-left: 20px;" valign="top">
                                                                                <table align="center" border="0" cellpadding="0" cellspacing="0" class="divider_content" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-top: 0px solid #BBBBBB; width: 100%;" valign="top" width="100%">
                                                                                    <tbody>
                                                                                        <tr style="vertical-align: top;" valign="top">
                                                                                            <td style="word-break: break-word; vertical-align: top; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top"><span></span></td>
                                                                                        </tr>
                                                                                    </tbody>
                                                                                </table>
                                                                            </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            <!--[if (!mso)&(!IE)]><!-->
                                                            </div>
                                                        <!--<![endif]-->
                                                        </div>
                                                    </div>
                                                <!--[if (mso)|(IE)]></td></tr></table><![endif]-->
                                                <!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]-->
                                                </div>
                                            </div>
                                        </div>
                                        <div style="background-color:transparent;">
                                            <div class="block-grid" style="Margin: 0 auto; min-width: 320px; max-width: 640px; overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; background-color: #2b303a;">
                                                <div style="border-collapse: collapse;display: table;width: 100%;background-color:#2b303a;">
                                                    <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:transparent;"><tr><td align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:640px"><tr class="layout-full-width" style="background-color:#2b303a"><![endif]-->
                                                    <!--[if (mso)|(IE)]><td align="center" width="640" style="background-color:#2b303a;width:640px; border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent;" valign="top"><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 0px; padding-left: 0px; padding-top:0px; padding-bottom:0px;"><![endif]-->
                                                    <div class="col num12" style="min-width: 320px; max-width: 640px; display: table-cell; vertical-align: top; width: 640px;">
                                                        <div style="width:100% !important;">
                                                            <!--[if (!mso)&(!IE)]><!-->
                                                            <div style="border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; border-right:0px solid transparent; padding-top:0px; padding-bottom:0px; padding-right: 0px; padding-left: 0px;">
                                                                <!--<![endif]-->
                                                                <table border="0" cellpadding="0" cellspacing="0" class="divider" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top" width="100%">
                                                                    <tbody>
                                                                        <tr style="vertical-align: top;" valign="top">
                                                                            <td class="divider_inner" style="word-break: break-word; vertical-align: top; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px;" valign="top">
                                                                                <table align="center" border="0" cellpadding="0" cellspacing="0" class="divider_content" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-top: 4px solid #FDCB8D; width: 100%;" valign="top" width="100%">
                                                                                    <tbody>
                                                                                        <tr style="vertical-align: top;" valign="top">
                                                                                            <td style="word-break: break-word; vertical-align: top; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top"><span></span></td>
                                                                                        </tr>
                                                                                    </tbody>
                                                                                </table>
                                                                            </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                                <table cellpadding="0" cellspacing="0" class="social_icons" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt;" valign="top" width="100%">
                                                                    <tbody>
                                                                        <tr style="vertical-align: top;" valign="top">
                                                                            <td style="word-break: break-word; vertical-align: top; padding-top: 28px; padding-right: 10px; padding-bottom: 10px; padding-left: 10px;" valign="top">
                                                                                <table align="center" cellpadding="0" cellspacing="0" class="social_table" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-tspace: 0; mso-table-rspace: 0; mso-table-bspace: 0; mso-table-lspace: 0;" valign="top">
                                                                                    <tbody>
                                                                                        <tr align="center" style="vertical-align: top; display: inline-block; text-align: center;" valign="top">
                                                                                            <td style="word-break: break-word; vertical-align: top; padding-bottom: 0; padding-right: 5px; padding-left: 5px;" valign="top"><a href="https://www.facebook.com/barbeariaamizades/ " target="_blank"><img alt="Facebook" height="32" src="https://pngimage.net/wp-content/uploads/2018/05/facebook-png-logo-white-5.png" style="text-decoration: none; -ms-interpolation-mode: bicubic; height: auto; border: none; display: block;" title="Facebook" width="32"/></a></td>
                                                                                            <td style="word-break: break-word; vertical-align: top; padding-bottom: 0; padding-right: 5px; padding-left: 5px;" valign="top"><a href="https://www.instagram.com/barbeariaamizades/" target="_blank"><img alt="Instagram" height="32" src="https://www.delas.pt/files/2018/03/logo-instagram.png" style="text-decoration: none; -ms-interpolation-mode: bicubic; height: auto; border: none; display: block;" title="Instagram" width="30"/></a></td>
                                                                                        </tr>
                                                                                    </tbody>
                                                                                </table>
                                                                            </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                                <table border="0" cellpadding="0" cellspacing="0" class="divider" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top" width="100%">
                                                                    <tbody>
                                                                        <tr style="vertical-align: top;" valign="top">
                                                                            <td class="divider_inner" style="word-break: break-word; vertical-align: top; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; padding-top: 25px; padding-right: 40px; padding-bottom: 10px; padding-left: 40px;" valign="top">
                                                                                <table align="center" border="0" cellpadding="0" cellspacing="0" class="divider_content" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-top: 1px solid #555961; width: 100%;" valign="top" width="100%">
                                                                                    <tbody>
                                                                                        <tr style="vertical-align: top;" valign="top">
                                                                                            <td style="word-break: break-word; vertical-align: top; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top"><span></span></td>
                                                                                        </tr>
                                                                                    </tbody>
                                                                                </table>
                                                                            </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                                <!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 40px; padding-left: 40px; padding-top: 20px; padding-bottom: 30px; font-family: Tahoma, sans-serif"><![endif]-->
                                                                <div style="color:#555555;font-family:Montserrat, Trebuchet MS, Lucida Grande, Lucida Sans Unicode, Lucida Sans, Tahoma, sans-serif;line-height:1.2;padding-top:20px;padding-right:40px;padding-bottom:30px;padding-left:40px;">
                                                                    <div style="line-height: 1.2; font-size: 12px; font-family: Montserrat, Trebuchet MS, Lucida Grande, Lucida Sans Unicode, Lucida Sans, Tahoma, sans-serif; color: #555555; mso-line-height-alt: 14px;">
                                                                        <p style="font-size: 12px; line-height: 1.2; word-break: break-word; text-align: center; font-family: inherit; mso-line-height-alt: 14px; margin: 0;"><span style="color: #95979c; font-size: 12px;">Barbearia Amizades S &amp; D Copyright © 2020</span></p>
                                                                    </div>
                                                                </div>
                                                            <!--[if mso]></td></tr></table><![endif]-->
                                                            <!--[if (!mso)&(!IE)]><!-->
                                                            </div>
                                                        <!--<![endif]-->
                                                        </div>
                                                    </div>
                                                    <!--[if (mso)|(IE)]></td></tr></table><![endif]-->
                                                <!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]-->
                                                </div>
                                            </div>
                                        </div>
                                    <!--[if (mso)|(IE)]></td></tr></table><![endif]-->
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    <!--[if (IE)]></div><![endif]-->
                    </body>
            """.format(titulo=titulo, mensagem=mensagem)
        
        return corpo