from django import forms
from clientes.models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [ 'cpf', 'nome', 'telefone' ]
        widgets = {
            'cpf':      forms.TextInput(attrs={'class': 'form-control'}),
            'nome':     forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
        }