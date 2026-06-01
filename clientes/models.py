from django.db import models

# Create your models here.

class Cliente(models.Model):
    cpf = models.CharField(max_length=11, primary_key=True)
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=11)