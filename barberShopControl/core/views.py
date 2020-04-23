from django.shortcuts import render


def acesso(request):
    return render(request, 'login/acesso.html')

def recuperarSenha(request):
    return render(request, 'login/recuperarsenha.html')

def criarConta(request):
    return render(request, 'login/criarconta.html')

def dashboard(request):
    return render(request, 'minha-conta/dashboard.html')

def servicos(request):
    return render(request, 'minha-conta/servicos.html')