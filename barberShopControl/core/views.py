from django.shortcuts import render


def home(request):
    return render(request, 'institucional/index.html')


def entrar(request):
    return render(request, 'login/entrar.html')


def recuperarSenha(request):
    return render(request, 'login/recuperarsenha.html')


def criarConta(request):
    return render(request, 'login/criarconta.html')
