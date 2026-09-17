from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import CustomUser
from .forms import SchoolProfileForm, SchoolProfileEditForm, RechercheStaffForm, InscriptionStaffForm
from .models import StaffRole, SchoolStaff


@login_required
def creer_etablissement(request):

    if SchoolStaff.objects.filter(user=request.user).exists():
        messages.info(request, "Vous êtes déjà rattaché à un établissement.")
        return redirect("portal:dashboard")

    if request.method == "POST":
        form = SchoolProfileForm(request.POST)
        if form.is_valid():
            school = form.save()

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

            messages.success(request, "Établissement créé avec succès. Vous en êtes le Directeur.")
            return redirect("portal:dashboard")
    else:
        form = SchoolProfileForm()

    return render(request, "configuration/creer_etablissement.html", {"form": form})


@login_required
def modifier_etablissement(request):
    """
    Permet au staff de compléter/modifier les informations de
    l'établissement : logo, cachet, coordonnées, devise...
    """

    school_staff = SchoolStaff.objects.filter(user=request.user).select_related("school").first()

    if not school_staff:
        messages.error(request, "Vous devez d'abord créer ou rejoindre un établissement.")
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