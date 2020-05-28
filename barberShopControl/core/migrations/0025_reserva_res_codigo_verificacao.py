# Generated by Django 3.0.5 on 2020-05-26 17:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_reserva_res_observacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='res_codigo_verificacao',
            field=models.CharField(default=django.utils.timezone.now, max_length=254, verbose_name='Código de Verificação'),
            preserve_default=False,
        ),
    ]