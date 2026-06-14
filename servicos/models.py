from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Servico(models.Model):
    nome = models.CharField(unique=True, null=False, max_length=50)
    duracao = models.IntegerField(
        null=False,
        validators=[
            MinValueValidator(15),
            MaxValueValidator(480)
        ]
    )
    descricao = models.CharField(default="", null=False, max_length=100)