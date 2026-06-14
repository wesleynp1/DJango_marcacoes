from django.shortcuts import render, redirect
from .models import Servico
from .forms  import ServicoForm


def index(request):
    return render(request, "servicos/index.html", {"servicos": Servico.objects.all()})


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
            "form": ServicoForm(),
            "mensagem": mensagem
        }
    )

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
    
