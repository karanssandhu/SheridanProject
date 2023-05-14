from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("update", views.update, name="update"),
    path("addPrinter", views.AddPrinter, name="addPrinter"),
    path("printerWebPage", views.printerWebPage, name="printerWebPage"),
]