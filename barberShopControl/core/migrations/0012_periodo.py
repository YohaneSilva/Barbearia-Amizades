# Generated by Django 3.0.5 on 2020-05-16 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_remove_servico_serv_tempo_duracao'),
    ]

    operations = [
        migrations.CreateModel(
            name='Periodo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('per_especialista', models.CharField(max_length=60, verbose_name='Especialista')),
                ('per_periodo', models.CharField(max_length=60, verbose_name='Periodo')),
                ('per_status', models.CharField(choices=[('S', 'Sim'), ('N', 'Não')], max_length=1, verbose_name='Livre')),
            ],
        ),
    ]
