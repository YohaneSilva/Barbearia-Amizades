# -*- coding:utf-8 -*-
from django import forms
from .models import Usuario

   
class Registrar(forms.ModelForm):
    
    class Meta:
        model = Usuario
        fields = (
            'us_primeiro_nome',
            'us_segundo_nome',
            'us_email',
            'us_senha',
            'us_telefone',
            )

    
    