from django.db import models

class Servico(models.Model):
    nome = models.CharField(unique=True)
    duracao = models.IntegerField(null=False)
    descricao = models.CharField(default="")    