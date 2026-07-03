from django.test import TestCase
from django.contrib import auth
from django.shortcuts import reverse

class TesteLogin(TestCase):
    def setUp(self):
        auth.models.User.objects.create_user(username='test', password='123')

    def teste_login(self):
        resposta = self.client.get(reverse("login"))
        self.assertEqual(resposta.status_code, 200)

        resposta = self.client.post(reverse("login"),{"username":"test","password":"123"})
        self.assertEqual(resposta.status_code, 302)

    def teste_redirect_if_logged_in(self):
        user = auth.models.User.objects.create_user("teste", "teste@testando.com", "12345678")
        self.client.force_login(user)

        resposta = self.client.get(reverse("login"))
        reposta = self.assertEqual(resposta.status_code, 302)
