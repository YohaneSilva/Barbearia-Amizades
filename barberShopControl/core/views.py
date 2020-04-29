from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .forms import *
from .models import Servico

def acesso(request):
    return render(request, 'login/acesso.html')

def recuperarSenha(request):
    return render(request, 'login/recuperarsenha.html')

def criarConta(request):
    return render(request, 'login/criarconta.html')

def dashboard(request):
    return render(request, 'minha-conta/dashboard.html')

def servicosCadastrados(request):
    # Trazendo todos os registros da tabela Serviço
    servicos_cadastrados = Servico.objects.all()        

    # Filtrando os registros da tabela Serviço
    busca = request.GET.get('search')
    if busca:
        servicos_cadastrados = Servico.objects.filter(serv_nome__icontains=busca)
    
    contexto = {'servicos_cadastrados' : servicos_cadastrados}

    return render(request, 'minha-conta/servicos/lista.html', contexto)

def novoServico(request):
    form_servico = FormularioServico()

    if request.method == "POST":
        form_servico = FormularioServico(request.POST)
    
        if form_servico.is_valid():
            nome = form_servico.cleaned_data['serv_nome']
            tempo_duracao = form_servico.cleaned_data['serv_tempo_duracao']
            valor = form_servico.cleaned_data['serv_valor']
            
            novo_servico = Servico(serv_nome=nome, serv_tempo_duracao=tempo_duracao, serv_valor=valor)
            novo_servico.save()

            messages.success(request, 'Serviço cadastrado com sucesso.', extra_tags='alert-success')

            return redirect('novoServico')

        else:
            form_servico = FormularioServico()
            messages.success(request, 'Não foi possível cadastrar o serviço', extra_tags='alert-danger')
    
    contexto = {'form_servico' : form_servico}

    return render(request, 'minha-conta/servicos/cadastro.html', contexto)

def editarServico(request, id):
    instance = get_object_or_404(Servico, id=id)
    
    if request.method == "POST":
        form_servico = FormularioServico(request.POST, instance=instance)

        if form_servico.is_valid():
            instance = form_servico.save(commit=False)
            instance.save()

            # Mensagem de sucesso
            messages.success(request, 'Serviço alterado com sucesso.', extra_tags='alert-success')
        else:
            messages.error(request, 'Serviço não alterado.', extra_tags='alert-danger')
    else:
        form_servico = FormularioServico(instance=instance)

    contexto = {
        "id_servico_selecionado" : id,
        "instance" : instance,
        "form_servico" : form_servico
    }
    return render(request, 'minha-conta/servicos/editar.html', contexto)

def excluirServico(request, id):
    if request.method == "POST":
        print('>>>>>>>>>>CHEGUEI<<<<<<<<<<<')
        instance = Servico.objects.get(id=id)
        instance.delete()
        messages.success(request, 'Serviço excluído com sucesso.', extra_tags='alert-success')
        return redirect('servicosCadastrados')