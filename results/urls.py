from django.urls import path
from . import views

app_name = "results"

urlpatterns = [
    path("", views.choisir_resultats, name="choisir_resultats"),
    path("classe/<int:classe_id>/periode/<int:period_id>/calculer/", views.calculer_resultats, name="calculer_resultats"),
    path("classe/<int:classe_id>/periode/<int:period_id>/", views.liste_resultats, name="liste_resultats"),
    path("bulletin/<int:eleve_id>/<int:period_id>/", views.bulletin_eleve, name="bulletin_eleve"),
    path("bulletin/<int:eleve_id>/<int:period_id>/pdf/", views.bulletin_pdf, name="bulletin_pdf"),
    path("bulletin/<int:eleve_id>/<int:period_id>/conduite/", views.saisir_conduite, name="saisir_conduite"),
    path("bulletins/<int:eleve_id>/", views.bulletins_enfant, name="bulletins_enfant"),
]