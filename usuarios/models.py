from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    matricula = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Matrícula"
    )

    curso = models.CharField(
        max_length=100,
        verbose_name="Curso"
    )

    def __str__(self):
        return f"{self.first_name} - {self.matricula}"