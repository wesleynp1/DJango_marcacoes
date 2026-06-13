from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from datetime import datetime
from django.utils import timezone

from marcacoes.models import  Marcacao
from clientes.models import Cliente
from servicos.models import Servico

# Create your views here.
@login_required
def index(request):
    marcacoes = Marcacao.objects.all().order_by("-datahora")

    for marcacao in marcacoes:
        #formata o nome do cliente se houver
        if marcacao.cliente:
            marcacao.cliente.nome = marcacao.cliente.nome.title()

        #separa data e hora para exibição
        marcacao.data = timezone.localtime(marcacao.datahora).strftime('%d/%m/%Y')
        marcacao.hora = timezone.localtime(marcacao.datahora).strftime('%H:%M')

    return render(
        request,
        'marcacoes/index.html',
        {
            "marcacoes": marcacoes,
            "agora" : timezone.now()
        }
    )

@login_required
def add_marcacoes(request):
    if request.method == 'GET':
        return render(
        request,
        'marcacoes/add.html',
        {
            "servicos": Servico.objects.all(),
            "clientes": Cliente.objects.all(),
            "agora": timezone.now()
        }
    )
    elif request.method == 'POST':

        livre = request.POST["cliente"] == 'LIVRE'

        Marcacao.objects.create(
            datahora = timezone.make_aware(datetime.fromisoformat(request.POST['data']+"T"+request.POST['hora']+":00")),
            cliente  = Cliente.objects.get(cpf=request.POST['cliente']) if not livre else None,
            servico  = Servico.objects.get(id=request.POST['servico']) if not livre else None,
        )

        return redirect("index")
    else:
        return "error"

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

@login_required
def edit_marcacao(request, id : int):
    if request.method == 'GET':
        marcacoes = Marcacao.objects.get(id=id)
        marcacao_edit = Marcacao.objects.get(id=id)

        # separa data e hora
        marcacao_edit.data = timezone.localtime(marcacao_edit.datahora).strftime('%Y-%m-%d')
        marcacao_edit.hora = timezone.localtime(marcacao_edit.datahora).strftime('%H:%M')

        dados = {
            "clientes" : Cliente.objects.all(),
            "servicos" : Servico.objects.all(),
            "agora"    : timezone.now(),
            "marcacoes": marcacoes,
            "marcacao" : marcacao_edit,
        }

        return render(request, 'marcacoes/edit.html', dados)
    elif request.method == 'POST':

        marcacao = Marcacao.objects.get(id=id)

        #ajusta datahora
        marcacao.datahora = timezone.make_aware(datetime.fromisoformat(request.POST['data']+"T"+request.POST['hora']+":00"))

        #ajusta campo cliente e serviço
        if  request.POST["cliente"] != 'LIVRE':
            marcacao.cliente = Cliente.objects.get(cpf=request.POST['cliente'])
            marcacao.servico = Servico.objects.get(id=request.POST['servico'])
        else:
            marcacao.cliente = None

        marcacao.save()

        return redirect("index")
    else:
        return "error"