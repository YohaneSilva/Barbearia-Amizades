from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import View
from django.core import serializers

import smtplib
import hashlib
from email.mime.text import MIMEText
from datetime import date, datetime

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

    return redirect('usuariosCadastrados')

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
def usuariosCadastrados(request):
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
    instancia_usuario = get_object_or_404(Usuario, id=id)
    
    if request.method == "POST":
        nome = request.POST['nome-especialista']
        usuario = request.POST['usuario-especialista']
        senha = request.POST['senha-especialista']

        print(nome, usuario, senha)
        novo_usuario = Usuario(
            us_nome = nome,
            us_usuario = usuario,
            us_senha = senha
        )
        novo_usuario.save()

        # Mensagem de sucesso
        messages.success(request, 'Cadastro alterado com sucesso.', extra_tags='alert-success')
        contexto = {
            "id_usuario_selecionado" : id,
            "instancia_usuario" : instancia_usuario,
        }
        return render(request, 'minha-conta/conta/editar.html', contexto)

    contexto = {
        "id_usuario_selecionado" : id,
        "instancia_usuario" : instancia_usuario,
    }
    return render(request, 'minha-conta/conta/editar.html', contexto)

def excluirUsuario(request, id):
    if request.method == "POST":
        instance = Usuario.objects.get(id=id)
        instance.delete()
        messages.success(request, 'Cadastro excluído', extra_tags='alert-success')
        return redirect('usuariosCadastrados')

def agendamentosCadastrados(request):
    agendamentos_cadastrados = Reserva.objects.all()

    contexto = {
        'agendamentos_cadastrados' : agendamentos_cadastrados
    }

    return render(request, 'minha-conta/agenda/lista.html', contexto)

def cadastrarAgendamento(request):
    if request.method == "POST":
        data_enviada_por_email = request.POST['data-enviada-por-email']
        nome_cliente = request.POST['nome-cliente']
        nome_especialista = request.POST['nome-especialista']
        email_destino = request.POST['email-cliente']
        servicos = ', '.join(request.POST.getlist('servicos-selecionados'))
        assunto = 'Realizar Agendamento | Barbearia Amizades S & D'
        mensagem = """\
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
                                                                        <strong>Agendamento Realizado</strong>
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
                                                                        Olá <strong>{cliente}.</strong> 
                                                                        <br><br> 
                                                                        O agendamento do dia <strong>{data}</strong>, com o especialista <strong>{especialista}</strong>, foi efetuado com sucesso!
                                                                        <br><br>
                                                                        Os serviços reservados foram: <strong>{servico}</strong>.
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
            """.format(cliente=nome_cliente, data=data_enviada_por_email, especialista=nome_especialista, servico=servicos)
        # Separando a data por dia, mês e ano
        data = request.POST['data-enviada']
        data = data.replace('/', ' ')
        dia = data.split()[0]
        mes = data.split()[1]
        ano = data.split()[2]
        
        # Verificando se o mesmo cliente já não possui 
        # um agendamento na data selecionada
        reservas = Reserva.objects.filter(res_data_atendimento__year=ano, res_data_atendimento__month=mes, res_data_atendimento__day=dia)
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
        email_enviado = request.POST['email-cliente']
        novo_agendamento = Reserva(
            res_nome_cliente = request.POST['nome-cliente'],
            res_telefone_cliente = telefone,
            res_data_atendimento = data_formatada,
            res_periodo_atendimento = request.POST['periodo-atendimento'],
            res_email_cliente = email_enviado,
            res_especialista = request.POST['nome-especialista'],
            res_servicos = servicos
        )

        novo_agendamento.save()
        envioDeEmail(assunto, mensagem, email_destino)
        return redirect('agendamentosCadastrados')
    
    return render(request, 'minha-conta/agenda/cadastro.html')

def excluirAgendamento(request, id):
    if request.method == "POST":
        data_agendada = request.POST['data-agendada']
        nome_cliente = request.POST['nome-cliente']
        nome_especialista = request.POST['nome-especialista']
        email_destino = request.POST['email-cliente']
        assunto = 'Cancelar Agendamento | Barbearia Amizades S & D'
        mensagem = """\
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
                                                                        <strong>Agendamento Cancelado</strong>
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
                                                                        Olá <strong>{cliente}.</strong> <br><br> O agendamento para o dia <strong>{data}</strong>, com o especialista <strong>{especialista}</strong>, foi cancelado com sucesso.
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
            """.format(cliente=nome_cliente, data=data_agendada, especialista=nome_especialista)
        instance = Reserva.objects.get(id=id)
        instance.delete()
        envioDeEmail(assunto, mensagem, email_destino)
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
        ano = data.split()[0]
        mes = data.split()[1]
        dia = data.split()[2]
        data_enviada = '{dia}/{mes}/{ano}'.format(dia=dia, mes=mes, ano=ano)

        # Data formatada para exibir no formulário de agendamento
        # e e-mail informando o o agendamento realizado
        data_enviada_formatada = '{dia} de {mes} de {ano}'.format(dia=dia, mes=meses_ano[mes], ano=ano)

        # Pegando a data atual do computador e 
        # verificando se a data solicitada não é retroativa
        data_local = date.today()
        dia_local = data_local.strftime("%d")
        mes_local = data_local.strftime("%m")
        ano_local = data_local.strftime("%y")
        data_local = '{dia}/{mes}/{ano}20'.format(dia=dia_local, mes=mes_local, ano=ano_local)

        # Convertendo a data enviada em timestamp
        timestamp_data_enviada = datetime.strptime(data_enviada,  "%d/%m/%Y")
        timestamp_data_enviada = datetime.timestamp(timestamp_data_enviada)

        # Convertendo a data local em timestamp
        data_local = datetime.strptime(data_local,  "%d/%m/%Y")
        timestamp_data_local = datetime.timestamp(data_local)

        if timestamp_data_enviada < timestamp_data_local:
            messages.success(request, 'A data informada é inválida.', extra_tags='alert-danger')
            return redirect('cadastrarAgendamento')

        # Consultando todos os registros da data enviada    
        reservas = Reserva.objects.filter(res_data_atendimento__year=ano, res_data_atendimento__month=mes, res_data_atendimento__day=dia)

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
                'data_enviada_formatada' : data_enviada_formatada,
                'data_enviada' : data_enviada,
                'servicos_cadastrados' : servicos_cadastrados
            }
            return render(request, 'minha-conta/agenda/cadastro.html', contexto)
        
        contexto = {
            'periodos_chiquinho' : periodos_chiquinho,
            'periodos_sandrinho' : periodos_sandrinho,
            'sem_periodo_disponivel' : sem_periodo_disponivel,
            'data_enviada_formatada' : data_enviada_formatada,
            'data_enviada' : data_enviada,
            'servicos_cadastrados' : servicos_cadastrados
        }
        return render(request, 'minha-conta/agenda/cadastro.html', contexto)

    return render(request, 'minha-conta/agenda/cadastro.html')

def envioDeEmail(assunto, mensagem, email_destino):
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