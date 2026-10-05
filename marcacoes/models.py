from datetime import timedelta, timezone

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from clientes.models import Cliente
from servicos.models import Servico

class Marcacao(models.Model):
    id = models.AutoField(
        primary_key=True
    )

    datahora = models.DateTimeField(
        unique=True
    )

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

    def __str__(self):
        return f'{self.cliente.nome} marcado de {self.datahora} até {self.datahora + timedelta(minutes=self.servico.duracao)}'
    
    def clean(self):
        fim_desta_marcacao = self.datahora + timedelta(minutes=self.servico.duracao)

        possiveis_marcacoes_conflito = Marcacao.objects.filter(
            datahora__lt=fim_desta_marcacao,
            datahora__gte=self.datahora - timedelta(minutes=Servico.MAX_DURACAO),
        ).exclude(id=self.id)

        for marcacao_conflitante in possiveis_marcacoes_conflito:

            fim_marcacao_conflitante = (marcacao_conflitante.datahora + timedelta(minutes=marcacao_conflitante.servico.duracao))

            if fim_marcacao_conflitante > self.datahora:

                raise ValidationError(
                    f"Tem gente marcada nesse horário: cliente {marcacao_conflitante.cliente.nome}"
                    f" de { timezone.localtime(marcacao_conflitante.datahora).strftime('%H:%M %d/%m/%Y')}"
                    f" até {timezone.localtime(fim_marcacao_conflitante).strftime('%H:%M %d/%m/%Y')}"
                )

    def formataMarcacoesParaExibir(marcacoes):
            for marcacao in marcacoes:
                marcacao.cliente.nome = marcacao.cliente.nome.title()
    
                #separa data e hora para exibição
                marcacao.datahora = timezone.localtime(marcacao.datahora)
    
                marcacao.data_inicio = marcacao.datahora.strftime('%d/%m/%Y')
                marcacao.hora_inicio = marcacao.datahora.strftime('%H:%M')
    
                marcacao.duracao = marcacao.servico.duracao
    
                marcacao.data_fim = (marcacao.datahora + timedelta(minutes=marcacao.duracao)).strftime('%d/%m/%Y')
                marcacao.hora_fim = (marcacao.datahora + timedelta(minutes=marcacao.duracao)).strftime('%H:%M')
                
    def diaDaSemana(self):
        DIAS_DA_SEMANA = ("segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo")
        hoje = timezone.now().date()
        if self.datahora.date() == hoje:    
            return "hoje"
        elif self.datahora.date() == hoje+timedelta(days=1):
            return "amanhã"
        elif self.datahora.date() == hoje+timedelta(days=2):
            return "depois de amanhã"
        else:
            return DIAS_DA_SEMANA[self.datahora.weekday()]