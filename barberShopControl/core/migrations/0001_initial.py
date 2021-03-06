# Generated by Django 3.0.5 on 2020-05-01 16:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Especialista',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('us_data_alter', models.DateTimeField(auto_now=True, null=True)),
                ('us_situacao_conta', models.CharField(choices=[(True, 'Ativado'), (False, 'Desativado')], max_length=5, verbose_name='Habilitar/Desabilitar')),
                ('us_perfil', models.CharField(choices=[('C', 'Cliente'), ('E', 'Especialista'), ('A', 'Administrador')], max_length=1, verbose_name='Perfil')),
                ('us_primeiro_nome', models.CharField(max_length=15, verbose_name='Primeiro Nome')),
                ('us_segundo_nome', models.CharField(max_length=45, verbose_name='Sobrenome')),
                ('us_sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino')], max_length=1, verbose_name='Sexo')),
                ('us_email', models.EmailField(max_length=254, unique=True, verbose_name='E-mail')),
                ('us_senha', models.CharField(max_length=20, verbose_name='Senha')),
                ('us_telefone', models.CharField(blank=True, max_length=11, verbose_name='Telefone')),
                ('us_end_cep', models.CharField(blank=True, max_length=8)),
                ('us_end_logradouro', models.CharField(blank=True, max_length=100)),
                ('us_end_numero', models.CharField(blank=True, max_length=8)),
                ('us_end_complemento', models.CharField(blank=True, max_length=100)),
                ('us_end_bairro', models.CharField(blank=True, max_length=72)),
                ('us_end_cidade', models.CharField(blank=True, max_length=72)),
                ('us_end_uf', models.CharField(blank=True, max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Servico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serv_data_alter', models.DateTimeField(auto_now=True, null=True)),
                ('serv_nome', models.CharField(max_length=40, verbose_name='Nome')),
                ('serv_tempo_duracao', models.TimeField(verbose_name='Duração')),
                ('serv_valor', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Valor')),
                ('serv_alter_usuario_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='serv_alter_usuario_id', to='core.Usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('res_data_criacao', models.DateTimeField(auto_now_add=True)),
                ('res_data_reserva', models.DateTimeField()),
                ('res_nome_cliente', models.CharField(blank=True, max_length=60, null=True)),
                ('res_telefone', models.CharField(blank=True, max_length=11, null=True)),
                ('res_avaliacao', models.IntegerField(blank=True, null=True)),
                ('res_obs_avaliacao', models.TextField(blank=True)),
                ('res_atend_realizado', models.BooleanField()),
                ('res_obs_atend', models.TextField(blank=True)),
                ('res_atend_enc_usuario_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='res_atend_enc_usuario_id', to='core.Usuario')),
                ('res_espec_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='res_espec_id', to='core.Especialista')),
                ('res_servico_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='res_servico_id', to='core.Servico')),
                ('res_usuario_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='res_usuario_id', to='core.Usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Estabelecimento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estab_alter_data', models.DateTimeField(auto_now=True, null=True)),
                ('estab_cnpj', models.CharField(max_length=15, unique=True)),
                ('estab_razao_social', models.CharField(max_length=60)),
                ('estab_nome_fantasia', models.CharField(max_length=60)),
                ('estab_end_cep', models.CharField(max_length=8)),
                ('estab_end_logradouro', models.CharField(blank=True, max_length=100)),
                ('estab_end_numero', models.CharField(blank=True, max_length=8)),
                ('estab_end_complemento', models.CharField(blank=True, max_length=100)),
                ('estab_end_bairro', models.CharField(blank=True, max_length=72)),
                ('estab_end_cidade', models.CharField(blank=True, max_length=72)),
                ('estab_end_uf', models.CharField(blank=True, max_length=2)),
                ('estab_alter_usuario_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='estab_alter_usuario_id', to='core.Usuario')),
            ],
        ),
        migrations.AddField(
            model_name='especialista',
            name='espec_servico_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='espec_servico_id', to='core.Servico'),
        ),
        migrations.AddField(
            model_name='especialista',
            name='espec_usuario_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='espec_usuario_id', to='core.Usuario'),
        ),
        migrations.CreateModel(
            name='Dias_Funcionamento_Estab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('func_alter_data', models.DateTimeField(auto_now=True, null=True)),
                ('func_dia', models.CharField(choices=[('seg', 'Segunda'), ('ter', 'Terça'), ('qua', 'Quarta'), ('qui', 'Quinta'), ('sex', 'Sexta'), ('sab', 'Sábado'), ('dom', 'Domingo')], max_length=3)),
                ('func_hora_inicial', models.TimeField()),
                ('func_hora_final', models.TimeField()),
                ('func_alter_usuario_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='func_alter_usuario_id', to='core.Usuario')),
                ('func_estab_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='func_estab_id', to='core.Estabelecimento')),
            ],
        ),
        migrations.CreateModel(
            name='Dias_Atendimento_Espec',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('atend_data_alter', models.DateTimeField(auto_now=True, null=True)),
                ('atend_hora_inicial', models.TimeField()),
                ('atend_hora_final', models.TimeField()),
                ('atend_alter_usuario_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='atend_alter_usuario_id', to='core.Usuario')),
                ('atend_dias_func_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='atend_dias_func_id', to='core.Dias_Funcionamento_Estab')),
                ('atend_espec_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='atend_espec_id', to='core.Especialista')),
            ],
        ),
    ]
