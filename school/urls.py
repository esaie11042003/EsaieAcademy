from django.urls import path
from . import views

app_name = "school"

urlpatterns = [
    path("annees/", views.gerer_annees, name="gerer_annees"),
    path("annees/<int:pk>/modifier/", views.modifier_annee, name="modifier_annee"),
    path("annees/<int:pk>/activer/", views.activer_annee, name="activer_annee"),
    path("periodes/", views.gerer_periodes, name="gerer_periodes"),
    path("periodes/<int:pk>/modifier/", views.modifier_periode, name="modifier_periode"),
    path("periodes/<int:pk>/activer/", views.activer_periode, name="activer_periode"),
]