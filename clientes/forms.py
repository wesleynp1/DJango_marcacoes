from django import forms
from clientes.models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente

        #determina quais campos e a ordem de exibição
        fields = [ 'nome', 'cpf', 'telefone' ]

        labels = {
            "cpf" : "CPF  (apenas números)",
            "telefone" : "Telefone   (apenas números)"
        }

        widgets = {
            'cpf':      forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'inputmode': 'numeric',
                'pattern' : '[0-9]*'
            }),

            'nome':     forms.TextInput(attrs={
                'class': 'form-control  mb-3',
            }),

            'telefone': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'inputmode': 'numeric',
                'pattern' : '[0-9]*'
            }),
        }