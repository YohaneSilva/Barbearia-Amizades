# Generated by Django 3.0.5 on 2020-05-01 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='us_situacao_conta',
            field=models.CharField(choices=[('A', 'Ativado'), ('D', 'Desativado')], max_length=1, verbose_name='Habilitar/Desabilitar'),
        ),
    ]
