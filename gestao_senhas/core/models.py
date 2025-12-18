from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone
import hashlib

def validar_nif(nif):
    """Valida NIF português"""
    if len(nif) != 9 or not nif.isdigit():
        return False
    total = sum([(int(nif[i]) * (9 - i)) for i in range(8)])
    control = 11 - (total % 11)
    if control >= 10:
        control = 0
    return control == int(nif[-1])

class Perfil(models.TextChoices):
    SUPERADMIN = 'superadmin', 'SuperAdmin'
    ADMIN = 'admin', 'Admin'
    USER = 'user', 'User'
    VIEWER = 'viewer', 'Viewer'

class TipoEmpresa(models.TextChoices):
    TECNIMPOR = 'tecnimpor', 'Tecnimpor (Interno)'
    CLIENTE = 'cliente', 'Cliente'

class Pais(models.Model):
    codigo = models.CharField(max_length=3, unique=True)
    designacao = models.CharField(max_length=100)

    class Meta:
        verbose_name = "País"
        verbose_name_plural = "Países"
        ordering = ['designacao']

    def save(self, *args, **kwargs):
        self.designacao = self.designacao.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codigo} - {self.designacao}"

class Cliente(models.Model):
    nif = models.CharField(max_length=9, unique=True, verbose_name="NIF")
    designacao_social = models.CharField(max_length=200)
    designacao_comercial = models.CharField(max_length=200, blank=True, null=True)
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT)
    email = models.EmailField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    morada = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['designacao_social']

    def clean(self):
        if not validar_nif(self.nif):
            raise ValidationError({'nif': 'NIF inválido'})

    def save(self, *args, **kwargs):
        self.full_clean()
        self.designacao_social = self.designacao_social.upper()
        if self.designacao_comercial:
            self.designacao_comercial = self.designacao_comercial.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nif} - {self.designacao_social}"

class Usuario(AbstractUser):
    perfil = models.CharField(max_length=20, choices=Perfil.choices, default=Perfil.USER)
    tipo_empresa = models.CharField(max_length=20, choices=TipoEmpresa.choices, default=TipoEmpresa.TECNIMPOR)
    empresa_cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, null=True, blank=True, related_name='usuarios')

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def clean(self):
        # Se tipo é cliente, empresa_cliente é obrigatória
        if self.tipo_empresa == TipoEmpresa.CLIENTE and not self.empresa_cliente:
            raise ValidationError({'empresa_cliente': 'Empresa cliente obrigatória para tipo Cliente'})

        # Se tipo é Tecnimpor, não pode ter empresa_cliente
        if self.tipo_empresa == TipoEmpresa.TECNIMPOR:
            self.empresa_cliente = None

        # Viewers devem ser sempre de clientes
        if self.perfil == Perfil.VIEWER and self.tipo_empresa != TipoEmpresa.CLIENTE:
            raise ValidationError({'tipo_empresa': 'Viewers devem ser de clientes'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        empresa = f" - {self.empresa_cliente}" if self.empresa_cliente else " - Tecnimpor"
        return f"{self.username} ({self.get_perfil_display()}){empresa}"

class Marca(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"
        ordering = ['nome']

    def save(self, *args, **kwargs):
        self.nome = self.nome.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

class Modelo(models.Model):
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Modelo"
        verbose_name_plural = "Modelos"
        unique_together = ['marca', 'nome']
        ordering = ['marca', 'nome']

    def save(self, *args, **kwargs):
        self.nome = self.nome.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.marca} {self.nome}"

class TipoControlador(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    tipo_senha = models.CharField(
        max_length=15,
        choices=[
            ('alfanumerica', 'Alfanumérica (Letras + Números)'),
            ('numerica', 'Numérica (Apenas Números)')
        ],
        default='alfanumerica',
        verbose_name='Tipo de Senha Permitida',
        help_text='Define se o controlador aceita senhas alfanuméricas ou apenas numéricas'
    )

    class Meta:
        verbose_name = "Tipo de Controlador"
        verbose_name_plural = "Tipos de Controladores"
        ordering = ['nome']

    def save(self, *args, **kwargs):
        self.nome = self.nome.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_senha_display()})"

class VersaoControlador(models.Model):
    tipo_controlador = models.ForeignKey(TipoControlador, on_delete=models.CASCADE)
    versao = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Versão de Controlador"
        verbose_name_plural = "Versões de Controladores"
        unique_together = ['tipo_controlador', 'versao']
        ordering = ['tipo_controlador', 'versao']

    def __str__(self):
        return f"{self.tipo_controlador} v{self.versao}"

class ModeloControlador(models.Model):
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE)
    versao_controlador = models.ForeignKey(VersaoControlador, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Modelo + Controlador"
        verbose_name_plural = "Modelos + Controladores"
        unique_together = ['modelo', 'versao_controlador']

    def __str__(self):
        return f"{self.modelo} com {self.versao_controlador}"

class Equipamento(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='equipamentos')
    modelo_controlador = models.ForeignKey(ModeloControlador, on_delete=models.PROTECT)
    numero_serie = models.CharField(max_length=100, verbose_name="Número de Série")
    notas = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Equipamento"
        verbose_name_plural = "Equipamentos"
        unique_together = ['modelo_controlador', 'numero_serie']
        ordering = ['cliente', 'numero_serie']

    def __str__(self):
        return f"{self.modelo_controlador} - SN: {self.numero_serie}"

class Senha(models.Model):
    TIPO_CHOICES = [
        ('definitiva', 'Definitiva'),
        ('temporaria', 'Temporária')
    ]

    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE, related_name='senhas')
    senha = models.CharField(max_length=12, unique=True, verbose_name="Senha (12 caracteres)")
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, default='definitiva')
    data_inicio = models.DateField(verbose_name="Data Início")
    data_fim = models.DateField(null=True, blank=True, verbose_name="Data Fim")
    ativa = models.BooleanField(default=True)
    criado_por = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='senhas_criadas')
    criado_em_data = models.DateField()
    criado_em_hora = models.TimeField()

    class Meta:
        verbose_name = "Senha"
        verbose_name_plural = "Senhas"
        ordering = ['-criado_em_data', '-criado_em_hora']

    def clean(self):
        if self.tipo == 'temporaria' and not self.data_fim:
            raise ValidationError({'data_fim': 'Data fim obrigatória para senhas temporárias'})
        if self.tipo == 'definitiva':
            self.data_fim = None
        if len(self.senha) > 12:
            raise ValidationError({'senha': 'Senha não pode ter mais de 12 caracteres'})

    @staticmethod
    def gerar_senha_automatica(equipamento):
        nif = equipamento.cliente.nif
        marca = equipamento.modelo_controlador.modelo.marca.nome
        modelo = equipamento.modelo_controlador.modelo.nome
        numero_serie = equipamento.numero_serie
        dados = f"{nif}{marca}{modelo}{numero_serie}"
        hash_obj = hashlib.sha256(dados.encode('utf-8'))
        senha_completa = hash_obj.hexdigest()
        senha_12 = senha_completa[:12].upper()
        contador = 0
        senha_final = senha_12
        while Senha.objects.filter(senha=senha_final).exists():
            dados_com_timestamp = f"{dados}{timezone.now().timestamp()}{contador}"
            hash_obj = hashlib.sha256(dados_com_timestamp.encode('utf-8'))
            senha_final = hash_obj.hexdigest()[:12].upper()
            contador += 1
        return senha_final

    def __str__(self):
        return f"{self.senha} ({self.tipo})"

class HistoricoSenha(models.Model):
    ACAO_CHOICES = [
        ('criacao', 'Criação'),
        ('edicao', 'Edição')
    ]

    senha = models.ForeignKey(Senha, on_delete=models.CASCADE, related_name='historico')
    acao = models.CharField(max_length=20, choices=ACAO_CHOICES)
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    data = models.DateField()
    hora = models.TimeField()
    detalhes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Histórico de Senha"
        verbose_name_plural = "Históricos de Senhas"
        ordering = ['-data', '-hora']

    def __str__(self):
        return f"{self.acao} - {self.usuario.username} ({self.data} {self.hora})"
