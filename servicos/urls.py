from django.urls import path
from servicos import views

app_name = "servicos"
urlpatterns = [
    path("",views.index,name="index"),
    path("add", views.add_servico, name="add"),
    path("delete/<int:id>", views.delete_servico, name="delete"),
    path("edit/<int:id>", views.edit_servico, name="edit")
]