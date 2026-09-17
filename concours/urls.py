from django.urls import path
from . import views

app_name = "concours"

urlpatterns = [
    path("", views.liste_concours, name="liste_concours"),
    path("ajouter/", views.ajouter_epreuve, name="ajouter_epreuve"),
    path("gerer/", views.gerer_concours, name="gerer_concours"),
    path("<int:pk>/modifier/", views.modifier_epreuve, name="modifier_epreuve"),
    path("<int:pk>/basculer/", views.basculer_epreuve, name="basculer_epreuve"),
    path("<int:pk>/supprimer/", views.supprimer_epreuve, name="supprimer_epreuve"),
    path("corbeille/", views.corbeille_concours, name="corbeille_concours"),
    path("<int:pk>/restaurer/", views.restaurer_epreuve, name="restaurer_epreuve"),
    path("<int:pk>/supprimer-definitivement/", views.supprimer_definitivement_epreuve, name="supprimer_definitivement_epreuve"),
    path("desactivees/", views.epreuves_desactivees, name="epreuves_desactivees"),
    path("<int:pk>/telecharger/<str:type_fichier>/", views.telecharger, name="telecharger"),
]