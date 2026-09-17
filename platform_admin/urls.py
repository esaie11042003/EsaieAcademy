from django.urls import path
from . import views

app_name = "platform_admin"

urlpatterns = [
    path("", views.vue_ensemble, name="vue_ensemble"),
    path("admins/", views.gerer_admins, name="gerer_admins"),
    path("admins/inscrire/", views.inscrire_admin, name="inscrire_admin"),
    path("admins/<int:pk>/retirer/", views.retirer_admin, name="retirer_admin"),
    path("etablissements/", views.gerer_etablissements, name="gerer_etablissements"),
    path("etablissements/<int:pk>/basculer/", views.basculer_etablissement, name="basculer_etablissement"),
    path("etablissements/<int:pk>/", views.detail_etablissement, name="detail_etablissement"),
    path("logo-devise/", views.modifier_logo_devise, name="modifier_logo_devise"),
]