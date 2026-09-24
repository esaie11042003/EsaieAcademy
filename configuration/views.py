from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from accounts.models import CustomUser
from .forms import SchoolProfileForm, SchoolProfileEditForm, RechercheStaffForm, InscriptionStaffForm
from .models import StaffRole, SchoolStaff, SchoolProfile


def _est_super_admin(user):
    return user.is_authenticated and user.is_superuser


def _etablissement_valide_requis(school_staff):
    """Retourne True si l'établissement du school_staff est validé."""
    return school_staff and school_staff.school.statut_validation == "valide"


@login_required
def creer_etablissement(request):

    if SchoolStaff.objects.filter(user=request.user).exists():
        messages.info(request, "Vous êtes déjà rattaché à un établissement.")
        return redirect("portal:dashboard")

    if request.method == "POST":
        form = SchoolProfileForm(request.POST)
        if form.is_valid():
            school = form.save(commit=False)
            school.statut_validation = "en_attente"
            school.save()

            role_directeur, _ = StaffRole.objects.get_or_create(
                school=school,
                nom="Directeur",
                defaults={"ordre": 1}
            )

            SchoolStaff.objects.create(
                school=school,
                user=request.user,
                role=role_directeur
            )

            messages.success(
                request,
                "Votre établissement a été créé et est en attente de validation par l'administration générale. "
                "Vous recevrez l'accès complet une fois votre dossier validé."
            )
            return redirect("portal:dashboard")
    else:
        form = SchoolProfileForm()

    return render(request, "configuration/creer_etablissement.html", {"form": form})


@login_required
def modifier_etablissement(request):

    school_staff = SchoolStaff.objects.filter(user=request.user).select_related("school").first()

    if not school_staff:
        messages.error(request, "Vous devez d'abord créer ou rejoindre un établissement.")
        return redirect("portal:dashboard")

    if not _etablissement_valide_requis(school_staff):
        messages.warning(request, "Votre établissement est en attente de validation. Cette action sera disponible une fois validé.")
        return redirect("portal:dashboard")

    school = school_staff.school

    if request.method == "POST":
        form = SchoolProfileEditForm(request.POST, request.FILES, instance=school)
        if form.is_valid():
            form.save()
            messages.success(request, "Informations de l'établissement mises à jour.")
            return redirect("portal:dashboard")
    else:
        form = SchoolProfileEditForm(instance=school)

    return render(request, "configuration/modifier_etablissement.html", {
        "form": form,
        "school": school,
    })


@login_required
def gerer_administration(request):

    school_staff = SchoolStaff.objects.filter(user=request.user).select_related("school").first()

    if not school_staff:
        messages.error(request, "Vous devez d'abord créer ou rejoindre un établissement.")
        return redirect("portal:dashboard")

    if not _etablissement_valide_requis(school_staff):
        messages.warning(request, "Votre établissement est en attente de validation. Cette action sera disponible une fois validé.")
        return redirect("portal:dashboard")

    school = school_staff.school

    if request.method == "POST":
        form = RechercheStaffForm(request.POST)
        if form.is_valid():
            identifiant = form.cleaned_data["identifiant"]
            fonction = form.cleaned_data["fonction"]

            user = CustomUser.objects.filter(username=identifiant, role="staff").first()
            if not user:
                user = CustomUser.objects.filter(email=identifiant, role="staff").first()

            if not user:
                messages.error(request, "Aucun membre du personnel trouvé avec cet identifiant.")
            elif SchoolStaff.objects.filter(user=user).exists():
                messages.error(request, "Cette personne est déjà rattachée à un établissement.")
            else:
                role, _ = StaffRole.objects.get_or_create(
                    school=school,
                    nom=fonction,
                    defaults={"ordre": 2}
                )
                SchoolStaff.objects.create(school=school, user=user, role=role)
                messages.success(request, f"{user.get_full_name() or user.username} a été ajouté à l'administration.")
                return redirect("configuration:gerer_administration")
    else:
        form = RechercheStaffForm()

    administration = SchoolStaff.objects.filter(school=school).select_related("user", "role")

    return render(request, "configuration/gerer_administration.html", {
        "form": form,
        "school": school,
        "administration": administration,
    })


@login_required
def inscrire_staff(request):

    school_staff = SchoolStaff.objects.filter(user=request.user).select_related("school").first()

    if not school_staff:
        messages.error(request, "Vous devez d'abord créer ou rejoindre un établissement.")
        return redirect("portal:dashboard")

    if not _etablissement_valide_requis(school_staff):
        messages.warning(request, "Votre établissement est en attente de validation. Cette action sera disponible une fois validé.")
        return redirect("portal:dashboard")

    school = school_staff.school

    if request.method == "POST":
        form = InscriptionStaffForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "staff"
            user.save()

            role, _ = StaffRole.objects.get_or_create(
                school=school,
                nom=form.cleaned_data["fonction"],
                defaults={"ordre": 2}
            )
            SchoolStaff.objects.create(school=school, user=user, role=role)

            messages.success(
                request,
                f"Compte créé pour {user.get_full_name() or user.username}. "
                f"Identifiant : {user.username} — transmettez-lui le mot de passe choisi."
            )
            return redirect("configuration:gerer_administration")
    else:
        form = InscriptionStaffForm()

    return render(request, "configuration/inscrire_staff.html", {
        "form": form,
        "school": school,
    })


# ============================================================
#   VALIDATION DES ÉTABLISSEMENTS (réservé à l'administrateur général)
# ============================================================

@user_passes_test(_est_super_admin)
def etablissements_en_attente(request):
    etablissements = SchoolProfile.objects.filter(statut_validation="en_attente").order_by("-created_at")
    return render(request, "configuration/etablissements_en_attente.html", {
        "etablissements": etablissements,
    })


@user_passes_test(_est_super_admin)
def valider_etablissement(request, pk):
    school = get_object_or_404(SchoolProfile, pk=pk)
    school.statut_validation = "valide"
    school.actif = True
    school.save()
    messages.success(request, f"« {school.nom} » a été validé. Le directeur a maintenant accès complet.")
    return redirect("configuration:etablissements_en_attente")


@user_passes_test(_est_super_admin)
def rejeter_etablissement(request, pk):
    school = get_object_or_404(SchoolProfile, pk=pk)
    school.statut_validation = "rejete"
    school.actif = False
    school.save()
    messages.success(request, f"« {school.nom} » a été rejeté.")
    return redirect("configuration:etablissements_en_attente")


@user_passes_test(_est_super_admin)
def creer_etablissement_direct(request):
    """
    Permet à l'administrateur général de créer directement un établissement
    déjà validé, avec son directeur, sans passer par la validation.
    """
    if request.method == "POST":
        form_ecole = SchoolProfileForm(request.POST, prefix="ecole")
        form_directeur = InscriptionStaffForm(request.POST, prefix="directeur")

        if form_ecole.is_valid() and form_directeur.is_valid():
            school = form_ecole.save(commit=False)
            school.statut_validation = "valide"
            school.save()

            role_directeur, _ = StaffRole.objects.get_or_create(
                school=school,
                nom="Directeur",
                defaults={"ordre": 1}
            )

            user = form_directeur.save(commit=False)
            user.role = "staff"
            user.save()

            SchoolStaff.objects.create(school=school, user=user, role=role_directeur)

            messages.success(
                request,
                f"Établissement « {school.nom} » créé et validé. "
                f"Identifiant du directeur : {user.username} — transmettez-lui le mot de passe choisi."
            )
            return redirect("configuration:etablissements_en_attente")
    else:
        form_ecole = SchoolProfileForm(prefix="ecole")
        form_directeur = InscriptionStaffForm(prefix="directeur")

    return render(request, "configuration/creer_etablissement_direct.html", {
        "form_ecole": form_ecole,
        "form_directeur": form_directeur,
    })
