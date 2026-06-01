from django.urls import path

from marcacoes import views

app_name = "marcacoes"
urlpatterns = [
    path("add", views.add_marcacoes, name="add"),
    path("delete/<int:id>", views.delete_marcacao, name="delete"),
    path("edit/<int:id>", views.edit_marcacao, name="edit")
]