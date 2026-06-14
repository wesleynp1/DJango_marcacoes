from django import forms

from servicos.models import Servico


class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = [
            "nome",
            "duracao",
            "descricao"
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'duracao': forms.NumberInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows':3}),
        }
