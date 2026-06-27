from django.test import TestCase
from pip._internal.resolution.resolvelib import reporter

from .models import  Marcacao
from clientes.models import Cliente
from servicos.models import Servico
from django.utils import timezone
from datetime import datetime, timedelta
from django.urls import reverse
from django.contrib import auth

# Create your tests here.
class TestMarcacao(TestCase):
    def setUp(self):
        # CLIENTES
        cliente1 = Cliente.objects.create(
            cpf='12345678910',
            nome='Ana',
            telefone=21987451236
        )

        cliente2 = Cliente.objects.create(
            cpf='15365445911',
            nome='Bob',
            telefone=21978415327
        )

        # SERVICOS
        servico1 = Servico.objects.create(
            nome="Servico A",
            duracao=40,
            descricao='É um servico classe A'
        )

        servico2 = Servico.objects.create(
            nome="Servico B",
            duracao=60,
            descricao='É um servico classe B'
        )

        # MARCAÇÕES
        Marcacao.objects.create(
            cliente=cliente1,
            datahora= (timezone.now() + timedelta(hours=4)),
            servico = servico1
        )

        Marcacao.objects.create(
            cliente=cliente2,
            datahora=(timezone.now() + timedelta(hours=6)),
            servico=servico2
        )

        Marcacao.objects.create(
            cliente=cliente2,
            datahora=(timezone.now() + timedelta(hours=8)),
            servico = servico2
        )

        user = auth.models.User.objects.create_user("teste", "teste@testando.com", "12345678")
        self.client.force_login(user)

    def test_cliente(self):
        cliente = Cliente.objects.get(cpf='12345678910')
        self.assertEqual(cliente.nome, 'Ana')

        novo_cliente = Cliente.objects.create(
            cpf="16186843458",
            nome="Carla",
            telefone=22956458712
        )

        self.assertEqual(Cliente.objects.get(cpf=novo_cliente.cpf).nome, 'Carla')

    def test_marcacao_add(self):
        resposta = self.client.get(reverse("marcacoes:add"))
        self.assertEqual(resposta.status_code, 200)

        dados = {
            "servico" : Servico.objects.all().first().id,
            "cliente":  Cliente.objects.all().first().id,
            "date":"2026-11-06",
            "hora":"15:00"
        }

        resposta = self.client.post(reverse("marcacoes:add"), dados)
        self.assertEqual(resposta.status_code, 302)
        cliente = Cliente.objects.get(id=dados["cliente"])

        datahora_marcado = timezone.make_aware(datetime.fromisoformat(dados['date']+"T"+dados['hora']+":00"))
        marcacao = Marcacao.objects.get(datahora=datahora_marcado)
        marcacao.datahora = timezone.localtime(marcacao.datahora)

        self.assertEqual(marcacao.datahora.strftime("%Y-%m-%d"), dados["date"])
        self.assertEqual(marcacao.datahora.strftime("%H:%M"), dados["hora"])
        self.assertEqual(cliente.nome, "Ana")

    def test_marcacao_delete(self):
        marcacao = Marcacao.objects.all()[0]
        resposta = self.client.get( reverse("marcacoes:delete",kwargs={"id": marcacao.id}) )
        self.assertEqual(resposta.status_code, 200)

        resposta = self.client.post( reverse("marcacoes:delete",kwargs={"id": marcacao.id}) )

        self.assertEqual(Marcacao.objects.filter(id=1).count(),0)
        self.assertEqual(resposta.status_code,302)

    def test_marcacao_edit(self):
        marcacao = Marcacao.objects.all().first()
        resposta = self.client.get(reverse("marcacoes:edit",kwargs={"id":marcacao.id}))
        self.assertEqual(resposta.status_code, 200)

        nova_datahora = timezone.now() + timedelta(days =1,hours=5)
        dados = {
            "id" : marcacao.id,
            "date" : nova_datahora.strftime("%Y-%m-%d"),
            "hora" : nova_datahora.time(),
            "cliente" : Cliente.objects.all().first().id,
            "servico" : Servico.objects.all().first().id
        }

        resposta = self.client.post(reverse("marcacoes:edit",kwargs={"id":marcacao.id}),dados)
        self.assertEqual(resposta.status_code, 302)

        marcacao_editada = Marcacao.objects.get(id=marcacao.id)
        marcacao_editada.cliente.id = dados["cliente"]

    def test_marcacao_edit_curta_deferenca_de_horario(self):
        marcacao = Marcacao.objects.all().first()
        novahora = (marcacao.datahora + timedelta(minutes=15)).time()

        dados = {
            "date": marcacao.datahora.strftime("%Y-%m-%d"),
            "hora": novahora,
            "cliente": marcacao.cliente.id,
            "servico": marcacao.servico.id
        }

        resultado = self.client.post(reverse("marcacoes:edit",kwargs={"id":marcacao.id}),dados)
        self.assertEqual(resultado.status_code, 302)

    def test_marcacao_com_conflito(self):
        marcacoes = Marcacao.objects.all()
        marcacao = marcacoes.first()

        if marcacao is None:
            raise Exception("CPF da cliente ana foi alterado")
        else:
            dados = {
            "date": marcacao.datahora.strftime("%Y-%m-%d"),
            "hora": (marcacao.datahora + timedelta(minutes=90)).strftime("%H:%M"),
            "cliente": marcacao.cliente.id,
            "servico": marcacao.servico.id
            }

            resposta = self.client.post(reverse('marcacoes:edit',kwargs={"id":marcacao.id}), dados)

            self.assertEqual(resposta.status_code, 200)
            self.assertContains(resposta, "form")