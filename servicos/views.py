from django.shortcuts import render, redirect
from .models import Servico


def index(request):
    return render(request, "servicos/index.html", {"servicos": Servico.objects.all()})


def add_servico(request):
    if request.method == "GET":
        return render(request,"servicos/add.html")
    elif request.method == "POST":

        #toda validação necessária

        Servico.objects.create(
            nome = request.POST["nome"],
            duracao = request.POST["duracao"],
            descricao = request.POST["descricao"]
        )

        return redirect('servicos:index')
        
def edit_servico(request, id : int):
    if request.method == "GET":        
        return render(request,"servicos/edit.html", { "servico": Servico.objects.get(id=id)})
    elif request.method == "POST":
        servico = Servico.objects.get(id=id)
        
        servico.nome      = request.POST["nome"]
        servico.duracao   = int(request.POST["duracao"])
        servico.descricao = request.POST["descricao"]

        servico.save()

        return redirect("servicos:index")
    
def delete_servico(request, id : int):
    if request.method == 'GET':
        return render(request, "servicos/delete.html", {"servico":Servico.objects.get(id=id)})
    if request.method == 'POST':
        Servico.objects.get(id=id).delete()
        return redirect("servicos:index")
    
