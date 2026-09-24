from django.urls import path
from . import views

app_name = "configuration"

urlpatterns = [
    path("etablissement/creer/", views.creer_etablissement, name="creer_etablissement"),
    path("etablissement/modifier/", views.modifier_etablissement, name="modifier_etablissement"),
    path("administration/gerer/", views.gerer_administration, name="gerer_administration"),
    path("administration/inscrire/", views.inscrire_staff, name="inscrire_staff"),
    path("etablissements/en-attente/", views.etablissements_en_attente, name="etablissements_en_attente"),
    path("etablissements/<int:pk>/valider/", views.valider_etablissement, name="valider_etablissement"),
    path("etablissements/<int:pk>/rejeter/", views.rejeter_etablissement, name="rejeter_etablissement"),
    path("etablissements/creer-direct/", views.creer_etablissement_direct, name="creer_etablissement_direct"),
]
