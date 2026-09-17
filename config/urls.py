from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("configuration/", include("configuration.urls")),
    path("classes/", include("classes.urls")),
    path("teachers/", include("teachers.urls")),
    path("students/", include("students.urls")),
    path("school/", include("school.urls")),
    path("subjects/", include("subjects.urls")),
    path("assignments/", include("assignments.urls")),
    path("evaluations/", include("evaluations.urls")),
    path("concours/", include("concours.urls")),
    path("examens/", include("examens.urls")),
    path("", include("portal.urls")),
    path("plateforme/", include("platform_admin.urls")),
    path("documents/", include("documents.urls")),
    path("paiement/", include("monetisation.urls")),
    path("banque/", include("banque.urls")),
    path("messagerie/", include("messagerie.urls")),
    path("resultats/", include("results.urls")),
    path("maitre-etude/", include("repetition.urls")),
    path("forum/", include("forum.urls")),
]   

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)