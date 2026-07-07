from django import forms
from clientes.models import Cliente

class ClienteForm(forms.ModelForm):

    cpf = forms.CharField(max_length=14, label="CPF  (apenas números)", widget=forms.TextInput(attrs={
                'class': 'form-control mb-3 input-CPF',
                'inputmode': 'numeric',
                'maxlength' : 14
                })
            )

    class Meta:
        model = Cliente

        #determina quais campos e a ordem de exibição
        fields = [ 'nome', 'cpf', 'telefone' ]

        labels = {
            "telefone" : "Telefone   (apenas números)"
        }

        widgets = {
            'nome':     forms.TextInput(attrs={
                'class': 'form-control  mb-3',
            }),

            'telefone': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'inputmode': 'numeric',
                'pattern' : '[0-9]*',
                'maxlength' : 11
            }),
        }