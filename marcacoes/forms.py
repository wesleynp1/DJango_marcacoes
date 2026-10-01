from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, time, timedelta

from clientes.models import Cliente
from marcacoes.models import Marcacao
from servicos.models import Servico
from django.core.validators import MinValueValidator


class MarcacaoForm(forms.Form):
    _attrs_padrao = {'class': 'form-control'}

    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        to_field_name='id',
        widget=forms.Select(attrs= _attrs_padrao),
        empty_label=None
    )
    servico = forms.ModelChoiceField(
        queryset=Servico.objects.all(),
        to_field_name='id',
        widget=forms.Select(attrs= _attrs_padrao),
        empty_label=None
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'} | _attrs_padrao),
    )

    hora = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'} | _attrs_padrao)
    )


    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['datahora']=timezone.make_aware(datetime.combine(cleaned_data.get('date'),cleaned_data.get('hora')))

        return cleaned_data