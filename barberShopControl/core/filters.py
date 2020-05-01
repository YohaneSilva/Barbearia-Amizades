import django_filters

from .models import *

class FiltroUsuario(django_filters.FilterSet):
    
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