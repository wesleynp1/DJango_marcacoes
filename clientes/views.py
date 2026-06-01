from django.http import Http404
from django.shortcuts import render, redirect
from .models import Cliente
# Create your views here.

def index(request):
    clientes = Cliente.objects.all()
    return render(request,"clientes/index.html",{"clientes":clientes})

def add_cliente(request):
    if request.method == "GET":
        return render(request,"clientes/add.html")
    elif request.method == "POST":
        Cliente.objects.create(cpf=request.POST["cpf"],nome=request.POST["nome"],telefone=request.POST["telefone"])
        return redirect("clientes:index")
    else:
        raise Http404


def delete_clientes(request,cpf : str):
    if request.method == "GET":
        cliente = Cliente.objects.get(cpf=cpf)
        return render(request,"clientes/delete.html",{"cliente":cliente})
    elif request.method == "POST":
        Cliente.objects.get(cpf=cpf).delete()
        return redirect("clientes:index")
    else:
        raise Http404


def edit_clientes(request, cpf : str):
    if request.method == "GET":
        cliente = Cliente.objects.get(cpf=cpf)
        return render(request,"clientes/edit.html",{"cliente":cliente})
    elif request.method == "POST":
        cliente = Cliente.objects.get(cpf=cpf)
        cliente.telefone = request.POST["telefone"]
        cliente.nome = request.POST["nome"]
        cliente.save()
        return redirect("clientes:index")
    else:
        raise Http404