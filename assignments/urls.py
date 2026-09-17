from django.urls import path
from . import views

app_name = "assignments"

urlpatterns = [
    path("gerer/", views.gerer_affectations, name="gerer_affectations"),
]