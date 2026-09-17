from django.urls import path
from . import views

app_name = "teachers"

urlpatterns = [
    path("gerer/", views.gerer_enseignants, name="gerer_enseignants"),
    path("inscrire/", views.inscrire_enseignant, name="inscrire_enseignant"),
    path("mes-coordonnees/", views.mes_coordonnees, name="mes_coordonnees"),
    path("mes-ecoles/", views.mes_ecoles, name="mes_ecoles"),
    path("mes-ecoles/<int:school_id>/entrer/", views.entrer_ecole, name="entrer_ecole"),
    path("mes-ecoles/<int:school_id>/classes/", views.mes_classes, name="mes_classes"),
    path("acces/<int:access_id>/reinitialiser-pin/", views.reinitialiser_pin, name="reinitialiser_pin"),
]