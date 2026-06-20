from django import forms
from clientes.models import Cliente

class ClienteForm(forms.ModelForm):
    template_name = 'clientes/form_wnp.html'

    class Meta:
        model = Cliente
        fields = ['cpf', 'nome', 'telefone']
        labels = { "cpf":"CPF", "telefone" : "Telefone(apenas números)" }
        widgets = {
            'cpf':      forms.TextInput(attrs={'class': 'form-control'}),
            'nome':     forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control','maxlength': 11}),
        }