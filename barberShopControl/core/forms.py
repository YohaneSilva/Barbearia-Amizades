from django import forms

from .models import Servico


class FormularioServico(forms.ModelForm):

    class Meta:
        model = Servico
        fields = [
            'serv_nome', 
            'serv_tempo_duracao',
            'serv_valor'
        ]

