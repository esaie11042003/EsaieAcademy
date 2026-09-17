from django.urls import path
from . import views

app_name = "banque"

urlpatterns = [
    path("epreuves/", views.liste_epreuves, name="liste_epreuves"),
    path("epreuves/ajouter/", views.ajouter_epreuve, name="ajouter_epreuve"),
    path("epreuves/<int:pk>/modifier/", views.modifier_epreuve, name="modifier_epreuve"),
    path("epreuves/<int:pk>/basculer/", views.basculer_epreuve, name="basculer_epreuve"),
    path("epreuves/<int:pk>/supprimer/", views.supprimer_epreuve, name="supprimer_epreuve"),
    path("epreuves/corbeille/", views.corbeille_epreuves, name="corbeille_epreuves"),
    path("epreuves/<int:pk>/restaurer/", views.restaurer_epreuve, name="restaurer_epreuve"),
    path("epreuves/<int:pk>/supprimer-definitivement/", views.supprimer_definitivement_epreuve, name="supprimer_definitivement_epreuve"),
    path("epreuves/desactivees/", views.epreuves_desactivees, name="epreuves_desactivees"),
    path("epreuves/<int:pk>/telecharger/<str:type_fichier>/", views.telecharger_epreuve, name="telecharger_epreuve"),

    path("documents/", views.liste_documents_classe, name="liste_documents_classe"),
    path("documents/ajouter/", views.ajouter_document_classe, name="ajouter_document_classe"),
    path("documents/<int:pk>/modifier/", views.modifier_document_classe, name="modifier_document_classe"),
    path("documents/<int:pk>/basculer/", views.basculer_document_classe, name="basculer_document_classe"),
    path("documents/<int:pk>/supprimer/", views.supprimer_document_classe, name="supprimer_document_classe"),
    path("documents/corbeille/", views.corbeille_documents_classe, name="corbeille_documents_classe"),
    path("documents/<int:pk>/restaurer/", views.restaurer_document_classe, name="restaurer_document_classe"),
    path("documents/<int:pk>/supprimer-definitivement/", views.supprimer_definitivement_document_classe, name="supprimer_definitivement_document_classe"),
    path("documents/desactives/", views.documents_classe_desactives, name="documents_classe_desactives"),
    path("documents/<int:pk>/telecharger/", views.telecharger_document_classe, name="telecharger_document_classe"),
]