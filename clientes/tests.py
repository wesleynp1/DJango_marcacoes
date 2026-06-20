from datetime import datetime
from django.test import TestCase
from django.shortcuts import reverse, get_object_or_404
from django.utils import timezone

from servicos.models import Servico
from .models import Cliente
from marcacoes.models import Marcacao
from django.contrib import auth

# Create your tests here.
class testClientes(TestCase):
    def setUp(self):
        c1 = Cliente.objects.create(cpf='12345678910', nome='Ana', telefone=21987451236)
        c2 = Cliente.objects.create(cpf='15365445911', nome='Bob', telefone=21978415327)

        s1 = Servico.objects.create( nome='Servico A', duracao=40, descricao="Um bom serviço" )
        s2 = Servico.objects.create( nome='Servico B', duracao=60, descricao="Um excelente serviço")

        Marcacao.objects.create(
            cliente=c1,
            datahora= timezone.make_aware(datetime(2025,1,20,15,30,00)),
            servico=s1
        )

        Marcacao.objects.create(
            cliente=c2,
            datahora=timezone.make_aware(datetime(2026, 3, 25, 16, 35, 00)),
            servico=s2
        )

        user = auth.models.User.objects.create_user("teste", "teste@testando.com", "12345678")
        self.client.force_login(user)

    def test_index(self):
        resposta = self.client.get(reverse("index"))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Ana")
        self.assertContains(resposta, "Bob")

    def test_add_cliente(self):
        resposta = self.client.get(reverse("clientes:add"))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "form")
        self.assertContains(resposta, "CPF")
        self.assertContains(resposta, "Nome")
        self.assertContains(resposta, "Telefone")

        dados = {
            "cpf":"12345678915",
            "nome":"Julia",
            "telefone" : 2197458365
        }

        resposta = self.client.post(reverse("clientes:add"),dados)
        self.assertEqual(resposta.status_code, 302)

        clienteNovo = Cliente.objects.get(cpf=dados["cpf"])
        self.assertEqual(clienteNovo.nome, dados["nome"])
        self.assertEqual(clienteNovo.telefone, dados["telefone"])

    def test_delete_cliente(self):
        cliente_para_deletar = get_object_or_404(Cliente, cpf='12345678910')

        #formulario de deleção
        resposta = self.client.get(reverse("clientes:delete", kwargs={"id":cliente_para_deletar.id} ))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, cliente_para_deletar.nome)

        #deleção
        resposta = self.client.post(reverse("clientes:delete", kwargs={"id":cliente_para_deletar.id} ))
        self.assertEqual(resposta.status_code, 302)

        #certifica-se que não existe mais
        self.assertEqual(Cliente.objects.filter(id=cliente_para_deletar.id).count(), 0)

    def test_edit_cliente(self):
        cliente_para_editar = get_object_or_404(Cliente, cpf='12345678910')

        novos_dados_cliente = {
            "cpf": "12345678910", #imutável
            "nome": "Yudi",
            "telefone":1140028922
        }

        resposta = self.client.get(reverse("clientes:edit", kwargs={"id": cliente_para_editar.id}))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Ana")

        resposta = self.client.post(
            reverse("clientes:edit", kwargs={"id": cliente_para_editar.id}),
            novos_dados_cliente
        )

        self.assertEqual(resposta.status_code, 302)

        cliente_atualizado = Cliente.objects.get(cpf=novos_dados_cliente["cpf"])
        self.assertEqual(cliente_atualizado.nome, novos_dados_cliente["nome"])
        self.assertEqual(cliente_atualizado.telefone, novos_dados_cliente["telefone"])