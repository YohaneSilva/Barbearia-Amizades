# Generated by Django 3.0.5 on 2020-05-18 21:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_reserva_res_servicos'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='res_email_cliente',
            field=models.CharField(default=django.utils.timezone.now, max_length=254, verbose_name='E-mail Cliente'),
            preserve_default=False,
        ),
    ]
