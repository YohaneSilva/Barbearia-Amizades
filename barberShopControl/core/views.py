from django.shortcuts import render


def login(request):
    return render(request, 'login.html')

def recuperarSenha(request):
    return render(request, 'recuperarsenha.html')

def cadastroCliente(request):
    return render(request, 'cadastro.html')