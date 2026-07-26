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
            'duracao': forms.NumberInput(attrs={'class': 'form-control only-numbers'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows':3}),
        }

        labels = {
            'nome' : f'Nome (máximo {Servico.MAX_NOME_LENGTH})',
            'duracao' : f'Duração em Minutos (máximo {Servico.MAX_DURACAO}min)',
            'descricao' : f'Descrição (máximo {Servico.MAX_DESCRICAO_LENGTH})'
        }
