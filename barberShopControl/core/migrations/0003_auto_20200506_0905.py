# Generated by Django 3.0.5 on 2020-05-06 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200501_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dias_atendimento_espec',
            name='atend_espec_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='atend_espec_id', to='core.Usuario'),
        ),
        migrations.AlterField(
            model_name='dias_funcionamento_estab',
            name='func_dia',
            field=models.CharField(choices=[('seg', 'Segunda'), ('ter', 'Terça'), ('qua', 'Quarta'), ('qui', 'Quinta'), ('sex', 'Sexta'), ('sab', 'Sábado'), ('dom', 'Domingo')], max_length=3, verbose_name='Dia'),
        ),
        migrations.AlterField(
            model_name='dias_funcionamento_estab',
            name='func_hora_final',
            field=models.TimeField(verbose_name='Hora Final'),
        ),
        migrations.AlterField(
            model_name='dias_funcionamento_estab',
            name='func_hora_inicial',
            field=models.TimeField(verbose_name='Hora Inicial'),
        ),
        migrations.AlterField(
            model_name='estabelecimento',
            name='estab_cnpj',
            field=models.CharField(max_length=15, unique=True, verbose_name='CNPJ'),
        ),
        migrations.AlterField(
            model_name='estabelecimento',
            name='estab_end_bairro',
            field=models.CharField(blank=True, max_length=72, verbose_name='Bairro'),
        ),
        migrations.AlterField(
            model_name='estabelecimento',
            name='estab_end_cep',
            field=models.CharField(max_length=8, verbose_name='CEP'),
        ),
        migrations.AlterField(
            model_name='estabelecimento',
            name='estab_end_cidade',
            field=models.CharField(blank=True, max_length=72, verbose_name='Cidade'),
        ),
        migrations.AlterField(
            model_name='estabelecimento',
            name='estab_end_complemento',
            field=models.CharField(blank=True, max_length=100, verbose_name='Complemento'),
        ),
        migrations.AlterField(
            model_name='estabelecimento',
            name='estab_end_logradouro',
            field=models.CharField(blank=True, max_length=100, verbose_name='Logradouro'),
        ),
        migrations.AlterField(
            model_name='estabelecimento',
            name='estab_end_numero',
            field=models.CharField(blank=True, max_length=8, verbose_name='Número'),
        ),
        migrations.AlterField(
            model_name='estabelecimento',
            name='estab_end_uf',
            field=models.CharField(blank=True, max_length=2, verbose_name='UF'),
        ),
        migrations.AlterField(
            model_name='estabelecimento',
            name='estab_nome_fantasia',
            field=models.CharField(max_length=60, verbose_name='Nome Fantasia'),
        ),
        migrations.AlterField(
            model_name='estabelecimento',
            name='estab_razao_social',
            field=models.CharField(max_length=60, verbose_name='Razão Social'),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='res_espec_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='res_espec_id', to='core.Usuario'),
        ),
        migrations.DeleteModel(
            name='Especialista',
        ),
    ]
