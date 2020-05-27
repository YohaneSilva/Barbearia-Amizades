# Generated by Django 3.0.5 on 2020-05-27 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_auto_20200527_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='res_avaliacao',
            field=models.CharField(default='Sem avaliação', max_length=13, verbose_name='Avaliar Atendimento'),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='res_observacao',
            field=models.TextField(default='', verbose_name='Observações'),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='res_observacao_avaliacao',
            field=models.CharField(default='', max_length=254, verbose_name='Código de Verificação'),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='res_observacao_especialista',
            field=models.TextField(default='', verbose_name='Observações'),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='res_status',
            field=models.CharField(default='Ativo', max_length=9, verbose_name='Situação'),
        ),
    ]
