from django.urls import path
from . import views

app_name = "aset"

urlpatterns = [
    path("", views.aset_list, name="aset_list"),
    path("tambah/", views.aset_create, name="aset_create"),
    path("<int:pk>/edit/", views.aset_edit, name="aset_edit"),
]
