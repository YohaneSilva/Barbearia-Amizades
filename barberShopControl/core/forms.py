from django import forms

from .models import *


class FormularioEstabelecimento(forms.ModelForm):

    class Meta:
        model = Estabelecimento
        fields = [
            'estab_cnpj',
            'estab_razao_social',
            'estab_nome_fantasia',
            'estab_end_cep',
            'estab_end_logradouro',
            'estab_end_numero',
            'estab_end_complemento',
            'estab_end_bairro',
            'estab_end_cidade',
            'estab_end_uf'
        ]


class FormularioServico(forms.ModelForm):

    class Meta:
        model = Servico
        fields = [
            'serv_nome',
            'serv_valor'
        ]

class FormularioUsuario(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = [
            'us_nome',
            'us_usuario',
            'us_senha',
        ]