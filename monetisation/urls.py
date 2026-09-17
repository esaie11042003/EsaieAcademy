from django.urls import path
from . import views

app_name = "monetisation"

urlpatterns = [
    path("comptes/", views.gerer_comptes_reception, name="gerer_comptes_reception"),
    path("acheter/<str:app_label>/<str:model_name>/<int:pk>/", views.acheter, name="acheter"),
    path("mes-achats/", views.mes_achats, name="mes_achats"),
    path("espace-paiements/", views.espace_paiements, name="espace_paiements"),
    path("achat/<int:pk>/valider/", views.valider_achat, name="valider_achat"),
    path("achat/<int:pk>/rejeter/", views.rejeter_achat, name="rejeter_achat"),
    path("achat/<int:pk>/recu/", views.recu, name="recu"),
    path("achat/<int:pk>/annuler/", views.annuler_achat, name="annuler_achat"),
]