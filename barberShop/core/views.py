# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response,render, redirect
from django.http import HttpResponse
from barberShop.core.form import Registrar
from .models import Usuario
from django.urls import reverse


# Create your views here.
def index(request):
    return render(request,'barberShop/index.html')


def login(request):
    return render(request,'barberShop/acesso.html')

def recuperarSenha(request):
    return render(request, 'barberShop/recuperarsenha.html')

def cadastroUsuario(request):
    if request.method == 'POST':
        form = Registrar(request.POST)
        if form.is_valid():
            usuario = form.save()
            return redirect('acesso')
        else:
            return render(request, 'barberShop/criarconta.html', {'form': form})
    
    else:
        usuario = Registrar()
        return render(request, 'barberShop/criarconta.html', {'form': usuario})

def agenda(request):
    return HttpResponse("Agenda")