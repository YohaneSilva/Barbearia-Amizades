from django.shortcuts import render


def home(request):
    return render(request, 'institucional/index.html')


def acesso(request):
    return render(request, 'login/acesso.html')


def recuperarSenha(request):
    return render(request, 'login/recuperarsenha.html')


def criarConta(request):
    return render(request, 'login/criarconta.html')
