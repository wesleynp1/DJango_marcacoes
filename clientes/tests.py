from datetime import datetime
from django.test import TestCase
from django.shortcuts import reverse
from .models import Cliente
from marcacoes.models import Marcacao

# Create your tests here.
class testClientes(TestCase):
    def setUp(self):
        c1 = Cliente.objects.create(cpf='12345678910', nome='Ana', telefone='21987451236')
        c2 = Cliente.objects.create(cpf='15365445911', nome='Bob', telefone='21978415327')
        Marcacao.objects.create(cliente=c1,datahora= datetime(2025,1,20,15,30,00))
        Marcacao.objects.create(cliente=c2, datahora=datetime(2026, 3, 25, 16, 35, 00))

    def test_index(self):
        resposta = self.client.get(reverse("index"))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Ana")
        self.assertContains(resposta, "Bob")

    def test_add_cliente(self):
        resposta = self.client.get(reverse("clientes:add"))
        self.assertEqual(resposta.status_code, 200)

        dados = {
            "cpf":"12345678915",
            "nome":"Julia",
            "telefone":"2197458365"
        }

        reposta = self.client.post(reverse("clientes:add"),dados)
        self.assertEqual(reposta.status_code, 302)

        clienteNovo = Cliente.objects.get(cpf=dados["cpf"])
        self.assertEqual(clienteNovo.nome, dados["nome"])
        self.assertEqual(clienteNovo.telefone, dados["telefone"])

    def test_delete_cliente(self):
        dados_cliente = {"cpf":"12345678910", "nome":"Ana"}
        resposta = self.client.get(reverse("clientes:delete",kwargs={"cpf":dados_cliente["cpf"]}))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, dados_cliente["nome"])

        resposta = self.client.post(reverse("clientes:delete", kwargs={"cpf": dados_cliente["cpf"]}))
        self.assertEqual(resposta.status_code, 302)
        self.assertEqual(Cliente.objects.filter(cpf=dados_cliente["cpf"]).count(),0)

    def test_delete_cliente(self):
        novos_dados_cliente = {
            "cpf": "12345678910", #imutável
            "nome": "Yudi",
            "telefone":"1140028922"
        }

        resposta = self.client.get(reverse("clientes:edit", kwargs={"cpf": novos_dados_cliente["cpf"]}))
        self.assertEqual(resposta.status_code, 200)

        resposta = self.client.post(reverse("clientes:edit", kwargs={"cpf": novos_dados_cliente["cpf"]}),novos_dados_cliente)
        self.assertEqual(resposta.status_code, 302)

        cliente_atualizado = Cliente.objects.get(cpf=novos_dados_cliente["cpf"])
        self.assertEqual(cliente_atualizado.nome, novos_dados_cliente["nome"])
        self.assertEqual(cliente_atualizado.telefone, novos_dados_cliente["telefone"])