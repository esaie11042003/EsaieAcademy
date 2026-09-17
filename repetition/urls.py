from django.urls import path
from . import views

app_name = "repetition"

urlpatterns = [
    path("", views.deposer_demande, name="deposer_demande"),
    path("merci/", views.merci, name="merci"),
    path("suivre/", views.suivre_demande, name="suivre_demande"),
    path("mes-demandes/", views.mes_demandes, name="mes_demandes"),
    path("mes-demandes/<int:pk>/", views.suivre_fil_utilisateur, name="suivre_fil_utilisateur"),
    path("admin/", views.liste_demandes, name="liste_demandes"),
    path("admin/<int:pk>/", views.detail_demande, name="detail_demande"),
]