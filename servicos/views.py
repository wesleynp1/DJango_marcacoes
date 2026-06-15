from django.shortcuts import render, redirect, get_object_or_404
from .models import Servico
from .forms  import ServicoForm


def index(request):
    return render(
        request,
        "servicos/index.html",
        {"servicos": Servico.objects.all()})

def add_servico(request):
    mensagem = ''

    if request.method == "POST":
        formulario = ServicoForm(request.POST)

        if formulario.is_valid():
            Servico.objects.create(
                nome      = formulario.cleaned_data["nome"],
                duracao   = formulario.cleaned_data["duracao"],
                descricao = formulario.cleaned_data["descricao"]
            )

            return redirect('servicos:index')
        else:
            mensagem = "Erro de Preenchimento!"

    return render(
        request,
        "servicos/add.html",
        {
            "acao" : "add",
            "form": ServicoForm(),
            "mensagem": mensagem
        }
    )

def edit_servico(request, id : int):
    servico = get_object_or_404(Servico, id=id)
    mensagem = ""

    if request.method == "POST":
        formulario = ServicoForm(request.POST,instance=servico)

        if formulario.is_valid():
            servico.nome = formulario.cleaned_data["nome"]
            servico.duracao = formulario.cleaned_data["duracao"]
            servico.descricao = formulario.cleaned_data["descricao"]

            servico.save()

            return redirect("servicos:index")
        else:
            mensagem = "Erro de Preenchimento!"

    return render(
        request,
        "servicos/add.html",
        {
            "id" : id,
            "form" : ServicoForm(instance=servico),
            "mensagem": mensagem
        })

def delete_servico(request, id : int):
    servico = get_object_or_404(Servico,id=id)

    if request.method == 'POST':
        servico.delete()
        return redirect("servicos:index")
    else:
        return render(
            request,
            "servicos/delete.html",
            {"servico":servico}
        )

    
