from django.urls import path
from . import views

app_name = "classes"

urlpatterns = [
    path("creer/", views.creer_classe, name="creer_classe"),
    path("<int:pk>/modifier/", views.modifier_classe, name="modifier_classe"),
]