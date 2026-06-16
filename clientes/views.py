from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente
from django.contrib.auth.decorators import login_required
from clientes.forms import ClienteForm

@login_required
def index(request):
    return render(
        request,
        "clientes/index.html",
        {"clientes":Cliente.objects.all()}
    )

@login_required
def add_cliente(request):
    mensagem = ""

    if request.method == "POST":
        cliente = ClienteForm(request.POST)

        if cliente.is_valid():
            Cliente.objects.create(
                cpf=      cliente.cleaned_data["cpf"],
                nome=     cliente.cleaned_data["nome"],
                telefone= cliente.cleaned_data["telefone"]
            )

            return redirect("clientes:index")
        else:
            mensagem = 'Erro de preenchimento do formulario'

    return render(
        request,
        "clientes/add.html",
        {
            "acao" : "add",
            "form": ClienteForm(),
            "mensagem" : mensagem
        }
    )

@login_required
def delete_clientes(request, id : int):
    cliente = get_object_or_404(Cliente, id=id)

    if request.method == "POST":
        cliente.delete()
        return redirect("clientes:index")

    return render(request, "clientes/delete.html", {"cliente": cliente})

@login_required
def edit_clientes(request, id : int):
    cliente = get_object_or_404(Cliente, id=id)
    mensagem = ""

    if request.method == "POST":
        formulario = ClienteForm(request.POST, instance=cliente)

        if formulario.is_valid():
            Cliente.objects.filter(id=id).update(
                cpf = formulario.cleaned_data["cpf"],
                nome = formulario.cleaned_data["nome"],
                telefone = formulario.cleaned_data["telefone"]
            )

            return redirect("clientes:index")
        else:
            mensagem = 'Erro de preenchimento do formulário'

    return render(
        request,
        "clientes/add.html",
        {
            "id" : cliente.id,
            "form": ClienteForm(instance=cliente),
            "mensagem": mensagem
        }
    )