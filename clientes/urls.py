from django.urls import path

from clientes import views

app_name = "clientes"
urlpatterns = [
    path("",views.index,name="index"),
    path("add", views.add_cliente, name="add"),
    path("delete/<str:cpf>", views.delete_clientes, name="delete"),
    path("edit/<str:cpf>", views.edit_clientes, name="edit")
]