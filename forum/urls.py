from django.urls import path
from . import views

app_name = "forum"

urlpatterns = [
    path("", views.mes_forums, name="mes_forums"),
    path("<int:pk>/", views.forum_detail, name="forum_detail"),
    path("rejoindre/<str:token>/", views.rejoindre_forum, name="rejoindre_forum"),

    path("admin/", views.liste_forums, name="liste_forums"),
    path("admin/creer/", views.creer_forum, name="creer_forum"),
    path("admin/<int:pk>/modifier/", views.modifier_forum, name="modifier_forum"),
    path("admin/<int:pk>/supprimer/", views.supprimer_forum, name="supprimer_forum"),
    path("admin/<int:pk>/basculer/", views.basculer_forum, name="basculer_forum"),
    path("admin/<int:pk>/membres/", views.gerer_membres, name="gerer_membres"),
    path("admin/<int:pk>/retirer/<int:user_id>/", views.retirer_membre, name="retirer_membre"),
]