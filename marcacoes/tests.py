from django.test import TestCase
from .models import  Marcacao
from clientes.models import Cliente
from datetime import datetime
from django.urls import reverse
from django.contrib import auth

# Create your tests here.
class TestMarcacao(TestCase):
    def setUp(self):
        c1 = Cliente.objects.create(cpf='12345678910', nome='Ana', telefone='21987451236')
        c2 = Cliente.objects.create(cpf='15365445911', nome='Bob', telefone='21978415327')
        Marcacao.objects.create(cliente=c1,datahora= datetime(2025,1,20,15,30,00))
        Marcacao.objects.create(cliente=c2, datahora=datetime(2026, 3, 25, 16, 35, 00))

        user = auth.models.User.objects.create_user("teste", "teste@testando.com", "12345678")
        self.client.force_login(user)

    def test_cliente(self):
        cliente = Cliente.objects.get(cpf='12345678910')
        self.assertEqual(cliente.nome, 'Ana')

        novo_cliente = Cliente.objects.create(
            cpf="16186843458",
            nome="Carla",
            telefone="22956458712"
        )

        self.assertEqual(Cliente.objects.get(cpf=novo_cliente.cpf).nome, 'Carla')

    def test_marcacao(self):
        cliente = Cliente.objects.get(cpf='12345678910')
        marcacao = Marcacao.objects.get(cliente=cliente)

        self.assertEqual(marcacao.datahora.day, 20)

    def test_marcacao_cliente_null(self):
        marcacao = Marcacao.objects.create(datahora=datetime(2025,1,21,20,00))
        self.assertEqual(marcacao.cliente, None)
        self.assertIsNotNone(Marcacao.objects.get(id=marcacao.id))

    def test_marcacao_add(self):

        dados = {
            "cliente":"12345678910",
            "data":"2026-11-06",
            "hora":"15:00"
        }
        resposta = self.client.post(reverse("marcacoes:add"), dados)
        self.assertEqual(resposta.status_code, 302)
        cliente = Cliente.objects.get(cpf=dados["cliente"])

        datahora_marcado = datetime(2026,11,6,15,00)
        marcacao = Marcacao.objects.get(datahora=datahora_marcado)
        self.assertEqual(marcacao.datahora.strftime("%Y-%m-%d"), dados["data"])
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
        marcacao = Marcacao.objects.all()[0]
        resposta = self.client.get(reverse("marcacoes:edit",kwargs={"id":marcacao.id}))
        self.assertEqual(resposta.status_code, 200)
        dados = {
            "data" : "2026-08-03",
            "hora" : "15:00",
            "cliente" : "15365445911"
        }
        resposta = self.client.post(reverse("marcacoes:edit",kwargs={"id":marcacao.id}),dados)
        self.assertEqual(resposta.status_code, 302)

        marcacao_editada = Marcacao.objects.get(id=marcacao.id)
        marcacao_editada.cliente.cpf = dados["cliente"]