from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)

class Usuarios(admin.ModelAdmin):
    list_display = ['id', 'us_primeiro_nome', 'us_segundo_nome','us_email','us_data_alter' ]

