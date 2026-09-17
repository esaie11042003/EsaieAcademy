from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages

from accounts.models import CustomUser
from configuration.models import SchoolProfile, SchoolStaff
from students.models import Eleve
from teachers.models import Teacher, TeacherSchoolAccess
from classes.models import Classe
from subjects.models import Subject
from evaluations.models import Evaluation
from concours.models import EpreuveConcours
from examens.models import EpreuveExamen
from documents.models import Document
from repetition.models import DemandeMaitreEtude

from .forms import RechercheAdminForm, InscriptionAdminForm, PlatformBrandingForm
from .models import PlatformBranding


def _est_super_admin(user):
    return user.is_authenticated and user.is_superuser


@user_passes_test(_est_super_admin)
def vue_ensemble(request):

    nouvelles_demandes = DemandeMaitreEtude.objects.filter(statut="nouvelle").count()

    context = {
        "nb_etablissements": SchoolProfile.objects.count(),
        "nb_eleves": Eleve.objects.count(),
        "nb_enseignants": Teacher.objects.count(),
        "nb_utilisateurs": CustomUser.objects.count(),
        "nb_admins": CustomUser.objects.filter(role="admin").count(),
        "nb_epreuves_concours": EpreuveConcours.objects.count(),
        "nb_epreuves_examens": EpreuveExamen.objects.count(),
        "nb_documents": Document.objects.count(),
        "derniers_utilisateurs": CustomUser.objects.order_by("-created_at")[:8],
        "derniers_etablissements": SchoolProfile.objects.order_by("-created_at")[:5],
        "nouvelles_demandes": nouvelles_demandes,
    }

    return render(request, "platform_admin/vue_ensemble.html", context)


@user_passes_test(_est_super_admin)
def gerer_admins(request):

    if request.method == "POST":
        form = RechercheAdminForm(request.POST)
        if form.is_valid():
            identifiant = form.cleaned_data["identifiant"]

            user = CustomUser.objects.filter(username=identifiant).first()
            if not user:
                user = CustomUser.objects.filter(email=identifiant).first()

            if not user:
                messages.error(request, "Aucun compte trouvé avec cet identifiant.")
            elif user.role == "admin":
                messages.info(request, "Ce compte est déjà administrateur.")
            else:
                user.role = "admin"
                user.save()
                messages.success(request, f"{user.get_full_name() or user.username} est maintenant co-administrateur.")
                return redirect("platform_admin:gerer_admins")
    else:
        form = RechercheAdminForm()

    admins = CustomUser.objects.filter(role="admin")

    return render(request, "platform_admin/gerer_admins.html", {
        "form": form,
        "admins": admins,
    })


@user_passes_test(_est_super_admin)
def inscrire_admin(request):

    if request.method == "POST":
        form = InscriptionAdminForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "admin"
            user.save()
            messages.success(
                request,
                f"Compte administrateur créé pour {user.get_full_name() or user.username}. "
                f"Identifiant : {user.username} — transmettez-lui le mot de passe choisi."
            )
            return redirect("platform_admin:gerer_admins")
    else:
        form = InscriptionAdminForm()

    return render(request, "platform_admin/inscrire_admin.html", {"form": form})


@user_passes_test(_est_super_admin)
def retirer_admin(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)

    if user.is_superuser:
        messages.error(request, "Impossible de retirer l'administrateur général.")
        return redirect("platform_admin:gerer_admins")

    user.role = "staff"
    user.save()
    messages.success(request, f"{user.get_full_name() or user.username} n'est plus co-administrateur.")
    return redirect("platform_admin:gerer_admins")


@user_passes_test(_est_super_admin)
def gerer_etablissements(request):

    etablissements = SchoolProfile.objects.all().order_by("nom")

    return render(request, "platform_admin/gerer_etablissements.html", {
        "etablissements": etablissements,
    })


@user_passes_test(_est_super_admin)
def basculer_etablissement(request, pk):

    etablissement = get_object_or_404(SchoolProfile, pk=pk)
    etablissement.actif = not etablissement.actif
    etablissement.save()
    return redirect("platform_admin:gerer_etablissements")


@user_passes_test(_est_super_admin)
def detail_etablissement(request, pk):

    school = get_object_or_404(SchoolProfile, pk=pk)

    classes = Classe.objects.filter(school=school).prefetch_related("matieres")
    eleves = Eleve.objects.filter(classe__school=school).select_related("classe")
    enseignants = TeacherSchoolAccess.objects.filter(school=school).select_related("teacher__user")
    administration = SchoolStaff.objects.filter(school=school).select_related("user", "role")
    evaluations = Evaluation.objects.filter(assignment__classe__school=school).select_related(
        "assignment__subject", "assignment__classe"
    )

    matieres_ids = set()
    for c in classes:
        matieres_ids.update(c.matieres.values_list("id", flat=True))
    matieres = Subject.objects.filter(id__in=matieres_ids)

    context = {
        "school": school,
        "classes": classes,
        "eleves": eleves,
        "enseignants": enseignants,
        "administration": administration,
        "matieres": matieres,
        "nb_evaluations": evaluations.count(),
        "dernieres_evaluations": evaluations.order_by("-date")[:10],
    }

    return render(request, "platform_admin/detail_etablissement.html", context)


@login_required
def modifier_logo_devise(request):

    if not request.user.is_superuser:
        messages.error(request, "Accès réservé à l'administrateur général.")
        return redirect("portal:dashboard")

    branding = PlatformBranding.get_solo()

    if request.method == "POST":
        form = PlatformBrandingForm(request.POST, request.FILES, instance=branding)
        if form.is_valid():
            form.save()
            messages.success(request, "Logo de la devise du Bénin mis à jour.")
            return redirect("platform_admin:vue_ensemble")
    else:
        form = PlatformBrandingForm(instance=branding)

    return render(request, "platform_admin/modifier_logo_devise.html", {
        "form": form,
        "branding": branding,
    })