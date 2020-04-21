from django.shortcuts import render


def loginPrincipal(request):
    return render(request, 'login-principal.html')

def recuperarSenha(request):
    return render(request, 'login-recuperarsenha.html')

def criarConta(request):
    return render(request, 'login-criarconta.html')