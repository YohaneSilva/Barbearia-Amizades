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
    serv_nome = models.CharField("Nome", max_length=40)
    serv_valor = models.DecimalField("Valor", max_digits=7, decimal_places=2)

    def __str__(self):
        return self.serv_nome


class Usuario(models.Model):
    us_nome = models.CharField("Nome", max_length=60)
    us_usuario = models.CharField(max_length=20, verbose_name="Usuario")
    us_senha = models.CharField("Senha", max_length=20)

    def __str__(self):
        return self.us_nome


class Reserva(models.Model):
    res_data_realizacao = models.DateTimeField("Data Realização", auto_now=True, auto_now_add=False, null=True)
    res_nome_cliente = models.CharField("Nome Cliente", max_length=60)
    res_telefone_cliente = models.CharField("Telefone Cliente", max_length=11)
    res_data_atendimento = models.DateField("Data Atendimento")
    res_email_cliente = models.CharField("E-mail Cliente", max_length=254)
    res_periodo_atendimento = models.CharField("Periodo Atendimento", max_length=5)
    res_especialista = models.CharField("Especialista", max_length=60)
    res_servicos = models.TextField("Servicos")
    