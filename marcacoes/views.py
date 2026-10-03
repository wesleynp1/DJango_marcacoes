from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from marcacoes.models import  Marcacao
from clientes.models import Cliente
from servicos.models import Servico
from .forms import MarcacaoForm
from django.core.paginator import Paginator

# Create your views here.
@login_required
def index(request):
    marcacoes_futuras  = Marcacao.objects.filter(datahora__gte = timezone.now()).order_by( "datahora")
    marcacoes_passadas = Marcacao.objects.filter(datahora__lt  = timezone.now()).order_by("-datahora")    
    
    paginator = Paginator(object_list=marcacoes_passadas, per_page=10)
    numero_da_pagina = int(request.GET['pagina']) if 'pagina' in request.GET else 1
    marcacoes_passadas_pag = paginator.get_page(numero_da_pagina)

    Marcacao.formataMarcacoesParaExibir(marcacoes_futuras)
    Marcacao.formataMarcacoesParaExibir(marcacoes_passadas_pag)

    return render(
        request,
        'marcacoes/index.html',
        {
            "marcacoes_futuras"  : marcacoes_futuras,
            "marcacoes_passadas": marcacoes_passadas_pag,
            "total_de_paginas" : paginator.num_pages,
            "pagina_atual" : numero_da_pagina,
            "range_de_paginas" : range(1,paginator.num_pages+1),
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
        'marcacoes/form.html',
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
        'marcacoes/form.html',
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