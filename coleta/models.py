from django.db import models
from django.conf import settings


class Residuo(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    pontos = models.PositiveIntegerField(default=0)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class PontoColeta(models.Model):
    nome = models.CharField(max_length=100)
    localizacao = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class RegistroReciclagem(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    residuo = models.ForeignKey(
        Residuo,
        on_delete=models.CASCADE
    )

    ponto_coleta = models.ForeignKey(
        PontoColeta,
        on_delete=models.CASCADE
    )

    quantidade = models.PositiveIntegerField(default=1)

    data = models.DateTimeField(auto_now_add=True)

    confirmado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario} - {self.residuo} ({self.quantidade})"