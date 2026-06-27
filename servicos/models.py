from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Servico(models.Model):
    MAX_DURACAO = 480
    id = models.AutoField(primary_key=True)
    nome = models.CharField(unique=True, null=False, max_length=50)
    duracao = models.IntegerField(
        null=False,
        validators=[
            MinValueValidator(15),
            MaxValueValidator(MAX_DURACAO)
        ]
    )
    descricao = models.CharField(default="", null=False, max_length=100)

    def __str__(self):
        return f'{self.nome} - {self.duracao}min.'
