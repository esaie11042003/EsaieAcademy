from django.urls import path
from . import views

app_name = "evaluations"

urlpatterns = [
    path("gerer/", views.gerer_evaluations, name="gerer_evaluations"),
    path("<int:pk>/notes/saisir/", views.saisir_notes, name="saisir_notes"),
    path("<int:pk>/notes/", views.liste_notes, name="liste_notes"),
    path("note/<int:pk>/modifier/", views.modifier_note, name="modifier_note"),
    path("note/<int:pk>/supprimer/", views.supprimer_note, name="supprimer_note"),
        path("suivi-ecole/", views.suivi_ecole, name="suivi_ecole"),
    path("<int:pk>/historique/", views.historique_evaluation, name="historique_evaluation"),
]