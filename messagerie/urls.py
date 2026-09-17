from django.urls import path
from . import views

app_name = "messagerie"

urlpatterns = [
    path("", views.inbox, name="inbox"),
    path("nouvelle/", views.nouvelle_conversation, name="nouvelle_conversation"),
    path("contacter-admins/", views.contacter_admins, name="contacter_admins"),
    path("<int:pk>/", views.conversation_detail, name="conversation_detail"),
    path("rechercher/", views.rechercher_utilisateurs, name="rechercher_utilisateurs"),
        path("fichier/<int:pk>/telecharger/", views.telecharger_fichier, name="telecharger_fichier"),
]