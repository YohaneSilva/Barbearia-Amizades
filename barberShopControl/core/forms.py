from django import forms

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

    
