import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Residuo(models.Model):
    """Tipo de resíduo reciclável aceito nos pontos de coleta."""

    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    pontos = models.PositiveIntegerField(
        default=0,
        help_text="Pontos ganhos por unidade reciclada deste resíduo."
    )
    icone = models.CharField(
        max_length=10,
        blank=True,
        help_text="Emoji ou símbolo curto (ex.: ♻️)."
    )
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Resíduo"
        verbose_name_plural = "Resíduos"
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} ({self.pontos} pts)"


class PontoColeta(models.Model):
    """Ponto físico de coleta identificado por QR Code."""

    nome = models.CharField(max_length=100)
    localizacao = models.CharField(
        max_length=200,
        help_text="Ex.: Bloco B, próximo à cantina."
    )
    descricao = models.TextField(blank=True)
    codigo = models.UUIDField(
    default=uuid.uuid4,
    editable=False,
    db_index=True,
    help_text="Código único usado no QR Code."
)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ponto de Coleta"
        verbose_name_plural = "Pontos de Coleta"
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} — {self.localizacao}"


class RegistroReciclagem(models.Model):
    """Registro de um descarte feito por um estudante em um ponto."""

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="registros_reciclagem"
    )
    residuo = models.ForeignKey(
        Residuo,
        on_delete=models.PROTECT,
        related_name="registros"
    )
    ponto_coleta = models.ForeignKey(
        PontoColeta,
        on_delete=models.PROTECT,
        related_name="registros"
    )
    quantidade = models.PositiveIntegerField(default=1)
    pontos = models.PositiveIntegerField(
        default=0,
        help_text="Pontos calculados no momento do registro (snapshot)."
    )
    confirmado = models.BooleanField(
        default=True,
        help_text="Auditoria: admin pode invalidar um registro depois."
    )
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Registro de Reciclagem"
        verbose_name_plural = "Registros de Reciclagem"
        ordering = ["-data"]
        indexes = [
            models.Index(fields=["usuario", "-data"]),
        ]

    def save(self, *args, **kwargs):
        # Calcula os pontos automaticamente antes de salvar
        if self.residuo_id and self.quantidade:
            self.pontos = self.residuo.pontos * self.quantidade
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.usuario} — {self.quantidade}x {self.residuo.nome} ({self.pontos} pts)"