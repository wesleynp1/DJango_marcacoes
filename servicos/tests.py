from django.test import TestCase
from .models import Servico
from django.urls import reverse

class TesteServicos(TestCase):
    def setUp(self):
        Servico.objects.create(
            nome='Servico',
            duracao = 45,
            descricao = 'Servico em Python'
        )

    def test_setup_cumprido(self):
        self.assertGreater(Servico.objects.all().count(),0)

    def test_servico_mostrar(self):
       resposta = self.client.get(reverse("servicos:index"))
       self.assertEqual(resposta.status_code, 200)

    def test_servico_criar(self):
        resposta = self.client.get(reverse("servicos:add"))
        self.assertEqual(resposta.status_code, 200)

        dados = {
            "nome": "Testar app",
            "duracao": 45,
            "descricao": "Vê se ta funcionando"
        }

        resposta = self.client.post(reverse("servicos:add"),dados)
        self.assertEqual(resposta.status_code, 302)
        self.assertGreater(Servico.objects.filter(nome=dados["nome"]).count(), 0)

    def test_servico_criar_muito_curto(self):

        dados = {
            "nome": "Testar app",
            "duracao": 10,
            "descricao": "Vê se ta funcionando"
        }

        resposta = self.client.post(reverse("servicos:add"),dados)
        self.assertEqual(resposta.status_code,200)
        self.assertContains(resposta,"Erro de Preenchimento!")


    def test_servico_edit(self):
        s1 = Servico.objects.first()

        resposta = self.client.get(reverse("servicos:edit",kwargs={"id": s1.id}))
        self.assertEqual(resposta.status_code, 200)

        novosDados = {
            'nome'      : 'Servico editado',
            'duracao'   : 50,
            'descricao' : 'Servico em Python3'
        }

        resposta = self.client.post(reverse("servicos:edit",kwargs={"id": s1.id}),novosDados)
        self.assertEqual(resposta.status_code, 302)

        s1 = Servico.objects.get(nome=novosDados["nome"])
        self.assertEqual(s1.duracao, novosDados["duracao"])
        self.assertEqual(s1.nome, novosDados["nome"])
        self.assertEqual(s1.descricao, novosDados["descricao"])

    def test_servico_delete(self):
        s1 = Servico.objects.first()
        resposta = self.client.get(reverse("servicos:delete",kwargs={"id": s1.id}))
        self.assertEqual(resposta.status_code, 200)

        novosDados = {
            'nome' : 'Servico eliminado',
            'duracao' : 45,
            'descricao' : 'Servico eliminado'
        }

        resposta = self.client.post(reverse("servicos:delete",kwargs={"id":s1.id}),novosDados)
        self.assertEqual(resposta.status_code, 302)
        self.assertEqual(Servico.objects.filter(nome=s1.nome).count(), 0)