from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, timedelta
from django.utils import timezone

from marcacoes.models import  Marcacao
from clientes.models import Cliente
from servicos.models import Servico
from .form import MarcacaoForm

# Create your views here.
@login_required
def index(request):
    marcacoes = Marcacao.objects.all().order_by("-datahora")

    for marcacao in marcacoes:
        marcacao.cliente.nome = marcacao.cliente.nome.title()

        #separa data e hora para exibição
        marcacao.datahora = timezone.localtime(marcacao.datahora)

        marcacao.data_inicio = marcacao.datahora.strftime('%d/%m/%Y')
        marcacao.hora_inicio = marcacao.datahora.strftime('%H:%M')

        marcacao.duracao = marcacao.servico.duracao

        marcacao.data_fim = (marcacao.datahora + timedelta(minutes=marcacao.duracao)).strftime('%d/%m/%Y')
        marcacao.hora_fim = (marcacao.datahora + timedelta(minutes=marcacao.duracao)).strftime('%H:%M')


    return render(
        request,
        'marcacoes/index.html',
        {
            "marcacoes": marcacoes,
            "agora" : timezone.now()
        }
    )

@login_required
def add_marcacoes(request : HttpRequest):

    if request.method == 'POST':
        formulario = MarcacaoForm(request.POST)

        if formulario.is_valid():

            nova_marcacao = Marcacao(
                datahora = formulario.cleaned_data.get('datahora'),
                cliente  = formulario.cleaned_data.get('cliente'),
                servico  = formulario.cleaned_data.get('servico'),
            )

            try:
                nova_marcacao.clean()
                nova_marcacao.save()
                return redirect("index")

            except ValidationError as e:
                formulario.add_error(None,e)

    else:
        hoje = timezone.localtime(timezone.now())
        formulario = MarcacaoForm({
            'servico': Servico.objects.first(),
            'cliente': Cliente.objects.first(),
            'date': hoje.strftime('%Y-%m-%d'),
            'hora': hoje.strftime('%H:%M')
        })

    return render(
        request,
        'marcacoes/add.html',
        {'form' : formulario}
    )

@login_required
def edit_marcacao(request, id : int):
    marcacao_a_editar = get_object_or_404(Marcacao, id=id)

    if request.method == 'POST':
        formulario = MarcacaoForm(request.POST)#passar o id para o form

        if formulario.is_valid():
            marcacao_a_editar.datahora = formulario.cleaned_data.get('datahora')
            marcacao_a_editar.cliente  = formulario.cleaned_data.get('cliente')
            marcacao_a_editar.servico  = formulario.cleaned_data.get('servico')

            try:
                marcacao_a_editar.clean()
                marcacao_a_editar.save()

                return redirect("index")
            except ValidationError as e:
                formulario.add_error(None,e)
    else:
        marcacao_a_editar.datahora = timezone.localtime(marcacao_a_editar.datahora)

        dados = {
            "id": id,
            "cliente": marcacao_a_editar.cliente,
            "servico": marcacao_a_editar.servico,
            'date': marcacao_a_editar.datahora.strftime('%Y-%m-%d'),
            'hora': marcacao_a_editar.datahora.strftime('%H:%M')
        }

        formulario = MarcacaoForm(dados)

    return render(
        request,
        'marcacoes/add.html',
        {'form' : formulario }
    )

@login_required
def delete_marcacao(request, id : int):
    marcacao = Marcacao.objects.get(id=id)

    if request.method == 'POST':
        marcacao.delete()
        return redirect("index")
    else:
        return render(
            request,
            "marcacoes/delete.html",
            {"marcacao":marcacao}
        )