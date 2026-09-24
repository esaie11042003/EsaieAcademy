from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "accounts"

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="portal:accueil"),
        name="logout",
    ),
    path("signup/", views.inscription, name="signup"),
    path("admins/gerer/", views.gerer_admins, name="gerer_admins"),
    path("admins/inscrire/", views.inscrire_admin, name="inscrire_admin"),
    path("admins/<int:pk>/retirer/", views.retirer_admin, name="retirer_admin"),
    path("admins/<int:pk>/basculer/", views.basculer_statut_admin, name="basculer_statut_admin"),
    path("admins/<int:pk>/supprimer/", views.supprimer_admin, name="supprimer_admin"),
]
