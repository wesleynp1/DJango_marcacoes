from django.db import models

# Create your models here.

class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    cpf = models.CharField(max_length=11, unique=True, primary_key=False)
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=11)