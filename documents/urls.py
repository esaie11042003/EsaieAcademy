from django.urls import path
from . import views

app_name = "documents"

urlpatterns = [
    path("", views.liste_documents, name="liste_documents"),
    path("ajouter/", views.ajouter_document, name="ajouter_document"),
    path("<int:pk>/corrige/", views.gerer_corrige, name="gerer_corrige"),
    path("<int:pk>/modifier/", views.modifier_document, name="modifier_document"),
    path("<int:pk>/telecharger/<int:file_id>/", views.telecharger, name="telecharger"),
    path("<int:pk>/basculer/", views.basculer_document, name="basculer_document"),
    path("<int:pk>/supprimer/", views.supprimer_document, name="supprimer_document"),
    path("corbeille/", views.corbeille, name="corbeille"),
    path("<int:pk>/restaurer/", views.restaurer_document, name="restaurer_document"),
    path("<int:pk>/supprimer-definitivement/", views.supprimer_definitivement, name="supprimer_definitivement"),
    path("desactives/", views.documents_desactives, name="documents_desactives"),
]