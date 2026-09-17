from django.urls import path
from . import views

app_name = "configuration"

urlpatterns = [
    path("etablissement/creer/", views.creer_etablissement, name="creer_etablissement"),
    path("etablissement/modifier/", views.modifier_etablissement, name="modifier_etablissement"),
    path("administration/gerer/", views.gerer_administration, name="gerer_administration"),
    path("administration/inscrire/", views.inscrire_staff, name="inscrire_staff"),
]