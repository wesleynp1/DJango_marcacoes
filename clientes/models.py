from django.core.validators import MaxValueValidator
from django.db import models

# Create your models here.

class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    cpf = models.CharField(max_length=11, unique=True, primary_key=False)
    nome = models.CharField(max_length=100)
    telefone = models.BigIntegerField(validators=[MaxValueValidator(99_99999_9999)])

    def __str__(self):
        return self.nome