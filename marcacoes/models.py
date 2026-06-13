from django.db import models
from clientes.models import Cliente
from servicos.models import Servico
# Create your models here

class Marcacao(models.Model):
    datahora = models.DateTimeField(unique=True)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.SET_NULL,
        default=None,
        null=True,
        blank=True
    )
    servico = models.ForeignKey(
        Servico,
        on_delete=models.SET_NULL,
        default=None,
        null=True,
        blank=True
    )