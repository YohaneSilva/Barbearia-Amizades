from django.db import models

class Estabelecimento(models.Model):
    estab_alter_data = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    estab_alter_usuario_id = models.ForeignKey("Usuario", related_name="estab_alter_usuario_id", on_delete=models.CASCADE, null=True)
    estab_cnpj = models.CharField("CNPJ", max_length=15, unique=True)
    estab_razao_social = models.CharField("Razão Social", max_length=60)
    estab_nome_fantasia = models.CharField("Nome Fantasia", max_length=60)
    estab_end_cep = models.CharField("CEP", max_length=8)
    estab_end_logradouro = models.CharField("Logradouro", max_length=100, blank=True)
    estab_end_numero = models.CharField("Número", max_length=8, blank=True)
    estab_end_complemento = models.CharField("Complemento", max_length=100, blank=True)
    estab_end_bairro = models.CharField("Bairro", max_length=72, blank=True)
    estab_end_cidade = models.CharField("Cidade", max_length=72, blank=True)
    estab_end_uf = models.CharField("UF", max_length=2, blank=True)


class Servico(models.Model):
    serv_data_alter = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    serv_alter_usuario_id = models.ForeignKey("Usuario", related_name="serv_alter_usuario_id", on_delete=models.CASCADE, null=True)
    serv_nome = models.CharField("Nome", max_length=40)
    serv_tempo_duracao = models.TimeField("Duração", auto_now=False, auto_now_add=False)
    serv_valor = models.DecimalField("Valor", max_digits=7, decimal_places=2)


class Usuario(models.Model):
    SEXO_CHOICES = (
        ("M", "Masculino"),
        ("F", "Feminino")
    )
        
    STATUS_CHOICES = (
        ("A", "Ativado"),
        ("D", "Desativado"),
    )

    us_data_alter = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    us_situacao_conta = models.CharField("Habilitar/Desabilitar", max_length=1, choices=STATUS_CHOICES)
    us_primeiro_nome = models.CharField("Primeiro Nome", max_length=15)
    us_segundo_nome = models.CharField("Sobrenome", max_length=45)
    us_sexo = models.CharField("Sexo", max_length=1, choices=SEXO_CHOICES)
    us_email = models.EmailField("E-mail", max_length=254, unique=True)
    us_senha = models.CharField("Senha", max_length=20)
    us_telefone = models.CharField("Telefone", max_length=11, blank=True)
    us_end_cep = models.CharField(max_length=8, blank=True)
    us_end_logradouro = models.CharField(max_length=100, blank=True)
    us_end_numero = models.CharField(max_length=8, blank=True)
    us_end_complemento = models.CharField(max_length=100, blank=True)
    us_end_bairro = models.CharField(max_length=72, blank=True)
    us_end_cidade = models.CharField(max_length=72, blank=True)
    us_end_uf = models.CharField(max_length=2, blank=True)


class Reserva(models.Model):
    res_data_criacao = models.DateTimeField(auto_now=False, auto_now_add=True)
    res_data_reserva = models.DateTimeField(auto_now=False, auto_now_add=False)
    res_usuario_id = models.ForeignKey("Usuario", related_name="res_usuario_id", on_delete=models.CASCADE, null=True)
    res_nome_cliente = models.CharField(max_length=60, blank=True, null=True)
    res_telefone = models.CharField(max_length=11, blank=True, null=True)
    res_espec_id = models.ForeignKey("Usuario", related_name="res_espec_id", on_delete=models.CASCADE)
    res_servico_id = models.ForeignKey("Servico", related_name="res_servico_id", on_delete=models.CASCADE)
    res_avaliacao = models.IntegerField(blank=True, null=True)
    res_obs_avaliacao = models.TextField(blank=True)
    res_atend_realizado = models.BooleanField()
    res_obs_atend = models.TextField(blank=True)
    res_atend_enc_usuario_id = models.ForeignKey("Usuario", related_name="res_atend_enc_usuario_id", on_delete=models.CASCADE, null=True)


class Dias_Funcionamento_Estab(models.Model):
    DIA_CHOICES = (
        ("seg", "Segunda"),
        ("ter", "Terça"),
        ("qua", "Quarta"),
        ("qui", "Quinta"),
        ("sex", "Sexta"),
        ("sab", "Sábado"),
        ("dom", "Domingo")
    )

    func_alter_data = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    func_alter_usuario_id = models.ForeignKey("Usuario", related_name="func_alter_usuario_id", on_delete=models.CASCADE, null=True)
    func_estab_id = models.ForeignKey("Estabelecimento", related_name="func_estab_id", on_delete=models.CASCADE)
    func_dia = models.CharField("Dia", max_length=3, choices=DIA_CHOICES)
    func_hora_inicial = models.TimeField("Hora Inicial", auto_now=False, auto_now_add=False)
    func_hora_final = models.TimeField("Hora Final", auto_now=False, auto_now_add=False)


class Dias_Atendimento_Espec(models.Model):
    atend_data_alter = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    atend_alter_usuario_id = models.ForeignKey("Usuario", related_name="atend_alter_usuario_id", on_delete=models.CASCADE, null=True)
    atend_espec_id = models.ForeignKey("Usuario", related_name="atend_espec_id", on_delete=models.CASCADE)
    atend_dias_func_id = models.ForeignKey("Dias_Funcionamento_Estab", related_name="atend_dias_func_id", on_delete=models.CASCADE)
    atend_hora_inicial = models.TimeField(auto_now=False, auto_now_add=False)
    atend_hora_final = models.TimeField(auto_now=False, auto_now_add=False)