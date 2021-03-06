# Generated by Django 3.0.5 on 2020-05-15 05:44

import datetime
from django.db import migrations, models
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20200514_1833'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dias_funcionamento_estab',
            name='func_alter_usuario_id',
        ),
        migrations.RemoveField(
            model_name='dias_funcionamento_estab',
            name='func_estab_id',
        ),
        migrations.RemoveField(
            model_name='reserva',
            name='res_atend_enc_usuario_id',
        ),
        migrations.RemoveField(
            model_name='reserva',
            name='res_espec_id',
        ),
        migrations.RemoveField(
            model_name='reserva',
            name='res_servico_id',
        ),
        migrations.RemoveField(
            model_name='reserva',
            name='res_usuario_id',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='us_data_alter',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='us_email',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='us_end_bairro',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='us_end_cep',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='us_end_cidade',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='us_end_complemento',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='us_end_logradouro',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='us_end_numero',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='us_end_uf',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='us_primeiro_nome',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='us_segundo_nome',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='us_sexo',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='us_situacao_conta',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='us_telefone',
        ),
        migrations.AddField(
            model_name='usuario',
            name='us_nome',
            field=models.CharField(default=datetime.datetime(2020, 5, 15, 5, 44, 32, 351146, tzinfo=utc), max_length=60, verbose_name='Nome'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='us_usuario',
            field=models.CharField(default=django.utils.timezone.now, max_length=20, verbose_name='Usuario'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Dias_Atendimento_Espec',
        ),
        migrations.DeleteModel(
            name='Dias_Funcionamento_Estab',
        ),
        migrations.DeleteModel(
            name='Reserva',
        ),
    ]
