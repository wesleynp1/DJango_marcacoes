from django.shortcuts import render, redirect
from datetime import datetime

from marcacoes.models import Cliente, Marcacao

# Create your views here.
def index(request):
    marcacoes = Marcacao.objects.all().order_by("-datahora")

    for marcacao in marcacoes:
        #formata o nome do cliente se houver
        if marcacao.cliente:
            marcacao.cliente.nome = marcacao.cliente.nome.title()

        #separa data e hora para exibição
        marcacao.data = marcacao.datahora.strftime('%d/%m/%Y')
        marcacao.hora = marcacao.datahora.strftime('%H:%M')

    return render(
        request,
        'marcacoes/index.html',
        {
            "marcacoes": marcacoes,
            "agora" : datetime.now()
        }
    )

def add_marcacoes(request):
    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        Marcacao.objects.create(
            datahora= datetime.fromisoformat(request.POST['data']+"T"+request.POST['hora']+":00"),
            cliente = Cliente.objects.get(cpf=request.POST['cliente']),
        )

        return redirect("index")
    else:
        return "error"
    return render(
        request,
        'marcacoes/add.html',
        {
            "clientes": Cliente.objects.all(),
            "agora": datetime.now()
        }
    )

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

def edit_marcacao(request, id : int):
    if request.method == 'GET':
        marcacoes = Marcacao.objects.get(id=id)
        marcacao_edit = Marcacao.objects.get(id=id)

        # separa data e hora
        marcacao_edit.data = marcacao_edit.datahora.strftime('%Y-%m-%d')
        marcacao_edit.hora = marcacao_edit.datahora.strftime('%H:%M')

        dados = {
            "clientes": Cliente.objects.all(),
            "agora": datetime.now(),
            "marcacoes": marcacoes,
            "marcacao" : marcacao_edit,
        }

        return render(request, 'marcacoes/edit.html', dados)

    elif request.method == 'POST':

        marcacao = Marcacao.objects.get(id=id)

        #ajusta datahora
        marcacao.datahora = datetime.fromisoformat(request.POST['data']+"T"+request.POST['hora']+":00")

        #ajusta campo cliente
        if  request.POST["cliente"] != 'LIVRE':
            marcacao.cliente = Cliente.objects.get(cpf=request.POST['cliente'])
        else:
            marcacao.cliente = None

        marcacao.save()

        return redirect("index")
    else:
        return "error"