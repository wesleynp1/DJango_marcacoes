from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import auth

def login(request):
    if request.method == "GET":
        next = request.GET["next"] if request.GET else ""
        return render(request,"login.html",{ "next" : next })
    elif request.method == "POST":
        user = auth.authenticate(request ,username=request.POST["username"], password=request.POST["password"])
        if user is not None:
            auth.login(request, user)
            return redirect("index")
        else:
            return render(request,"login.html",{"mensagem":"Autenticação falhou!"})
    else:
        raise Http404

@login_required
def logout(request):
    if request.method == "GET":
        return render(request,"logout.html")
    elif request.method == "POST":
        auth.logout(request)
        return redirect('index')

    else:
        raise Http404