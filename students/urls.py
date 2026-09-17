from django.urls import path
from . import views

app_name = "students"

urlpatterns = [
    path("gerer/", views.gerer_eleves, name="gerer_eleves"),
    path("inscrire/", views.inscrire_eleve, name="inscrire_eleve"),
    path("<int:pk>/modifier/", views.modifier_eleve, name="modifier_eleve"),
    path("<int:pk>/code-parent/", views.code_parent, name="code_parent"),
    path("lier-parent/", views.lier_parent, name="lier_parent"),
]