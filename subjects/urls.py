from django.urls import path
from . import views

app_name = "subjects"

urlpatterns = [
    path("gerer/", views.gerer_matieres, name="gerer_matieres"),
    path("<int:pk>/modifier/", views.modifier_matiere, name="modifier_matiere"),
]