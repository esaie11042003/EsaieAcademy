from django.urls import path
from . import views

app_name = "portal"

urlpatterns = [
    path("", views.accueil, name="accueil"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("choix-acces/", views.choix_acces, name="choix_acces"),
]