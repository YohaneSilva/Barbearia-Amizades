# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response,render, redirect
from django.http import HttpResponse
from barberShop.core.form import Registrar
from .models import Usuario
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse, reverse_lazy
from django.views import generic


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/criarconta.html'
    

# Create your views here.
def index(request):
    return render(request,'barberShop/index.html')


'''def login(request):
    return render(request,'registration/login.html')'''

def recuperarSenha(request):
    return render(request, 'barberShop/recuperarsenha.html')

def cadastroUsuario(request):
    if request.method == 'POST':
        form = Registrar(request.POST)
        if form.is_valid():
            usuario = form.save()
            return redirect('login')
        else:
            return render(request, 'barberShop/criarconta.html', {'form': form})
    
    else:
        usuario = Registrar()
        return render(request, 'barberShop/criarconta.html', {'form': usuario})

def agenda(request):
    return HttpResponse("Agenda")