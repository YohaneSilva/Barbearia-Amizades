# -*- coding: utf-8 -*-

from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import Servico, Usuario


class FormularioServico(forms.ModelForm):

    class Meta:
        model = Servico
        fields = [
            'serv_nome', 
            'serv_tempo_duracao',
            'serv_valor'
        ]

class FormularioConta(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = [
            'us_situacao_conta',
            'us_perfil',
            'us_primeiro_nome',
            'us_segundo_nome',
            'us_sexo',
            'us_email',
            'us_telefone'
        ]
        
class UserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password', 'is_staff']
        widgets = {
            'first_name': forms.TextInput(attrs={'required': True,'class': 'form-control', 'maxlength':20}),
            'last_name': forms.TextInput(attrs={'required': True,'class': 'form-control', 'maxlength':20}),
            'email': forms.TextInput(attrs={'required': True,'class': 'form-control', 'maxlength':254}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'maxlength':50}),
            'password': forms.PasswordInput(attrs={'type':'password','class': 'form-control', 'maxlength':20}),
            'is_staff': forms.TextInput(attrs={'class': 'form-control', 'maxlength':20 }),
            
        }    
        

