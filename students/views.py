from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from configuration.models import SchoolStaff
from accounts.models import CustomUser
from .forms import RechercheEleveForm, InscriptionEleveForm
from .models import Eleve
from .forms import EleveEditForm, CodeParentForm

@login_required
def gerer_eleves(request):

    school_staff = SchoolStaff.objects.filter(user=request.user).select_related("school").first()

    if not school_staff:
        messages.error(request, "Vous devez d'abord créer ou rejoindre un établissement.")
        return redirect("portal:dashboard")

    school = school_staff.school

    if request.method == "POST":
        form = RechercheEleveForm(request.POST, school=school)
        if form.is_valid():
            identifiant = form.cleaned_data["identifiant"]

            user = CustomUser.objects.filter(username=identifiant, role="student").first()
            if not user:
                user = CustomUser.objects.filter(email=identifiant, role="student").first()

            if not user:
                messages.error(request, "Aucun élève trouvé avec cet identifiant.")
            elif Eleve.objects.filter(user=user).exists():
                messages.error(request, "Cet élève est déjà rattaché à une classe.")
            else:
                Eleve.objects.create(
                    user=user,
                    matricule=form.cleaned_data["matricule"],
                    nom=user.last_name or user.username,
                    prenom=user.first_name or "",
                    sexe=user.sexe or "M",
                    date_naissance=user.date_naissance,
                    classe=form.cleaned_data["classe"],
                )
                messages.success(request, f"{user.get_full_name() or user.username} a été ajouté à l'établissement.")
                return redirect("students:gerer_eleves")
    else:
        form = RechercheEleveForm(school=school)

    eleves = Eleve.objects.filter(classe__school=school).select_related("classe")

    return render(request, "students/gerer_eleves.html", {
        "form": form,
        "school": school,
        "eleves": eleves,
    })


@login_required
def inscrire_eleve(request):

    school_staff = SchoolStaff.objects.filter(user=request.user).select_related("school").first()

    if not school_staff:
        messages.error(request, "Vous devez d'abord créer ou rejoindre un établissement.")
        return redirect("portal:dashboard")

    school = school_staff.school

    if request.method == "POST":
        form = InscriptionEleveForm(request.POST, school=school)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "student"
            user.save()

            Eleve.objects.create(
                user=user,
                matricule=form.cleaned_data["matricule"],
                nom=user.last_name,
                prenom=user.first_name,
                sexe=form.cleaned_data["sexe"],
                date_naissance=form.cleaned_data["date_naissance"],
                classe=form.cleaned_data["classe"],
            )

            messages.success(
                request,
                f"Compte créé pour {user.get_full_name() or user.username}. "
                f"Identifiant : {user.username} — transmettez-lui le mot de passe choisi."
            )
            return redirect("students:gerer_eleves")
    else:
        form = InscriptionEleveForm(school=school)

    return render(request, "students/inscrire_eleve.html", {
        "form": form,
        "school": school,
    })

@login_required
def modifier_eleve(request, pk):
    """
    Permet au staff de l'école de modifier les informations
    d'un élève (nom, statut, NPI, classe, etc.).
    """

    eleve = get_object_or_404(Eleve, pk=pk)

    if not eleve.classe or not SchoolStaff.objects.filter(
        user=request.user, school=eleve.classe.school
    ).exists():
        messages.error(request, "Vous n'êtes pas autorisé à modifier cet élève.")
        return redirect("portal:dashboard")

    if request.method == "POST":
        form = EleveEditForm(request.POST, instance=eleve)
        if form.is_valid():
            form.save()
            messages.success(request, f"Informations de {eleve.prenom} {eleve.nom} mises à jour.")
            return redirect("portal:dashboard")
    else:
        form = EleveEditForm(instance=eleve)

    return render(request, "students/modifier_eleve.html", {
        "form": form,
        "eleve": eleve,
    })


@login_required
def code_parent(request, pk):
    """
    Affiche le code de liaison parent d'un élève, et permet
    de le régénérer (invalide l'ancien code).
    """

    eleve = get_object_or_404(Eleve, pk=pk)

    if not eleve.classe or not SchoolStaff.objects.filter(
        user=request.user, school=eleve.classe.school
    ).exists():
        messages.error(request, "Vous n'êtes pas autorisé à voir ce code.")
        return redirect("portal:dashboard")

    if request.method == "POST":
        eleve.generer_code_parent()
        messages.success(request, "Nouveau code généré. L'ancien code ne fonctionne plus.")
        return redirect("students:code_parent", pk=eleve.pk)

    if not eleve.code_parent:
        eleve.generer_code_parent()

    return render(request, "students/code_parent.html", {
        "eleve": eleve,
    })


@login_required
def lier_parent(request):
    """
    Permet à un parent de lier un enfant à son compte
    via le code fourni par l'établissement.
    Limite : 2 parents maximum par élève.
    """

    if request.user.role != "parent":
        messages.error(request, "Cette fonctionnalité est réservée aux parents.")
        return redirect("portal:dashboard")

    if request.method == "POST":
        form = CodeParentForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            eleve = Eleve.objects.filter(code_parent=code).first()

            if not eleve:
                messages.error(request, "Aucun élève ne correspond à ce code.")
            elif eleve.parents.filter(pk=request.user.pk).exists():
                messages.info(request, f"{eleve.prenom} {eleve.nom} est déjà lié à votre compte.")
                return redirect("portal:dashboard")
            elif eleve.parents.count() >= 2:
                messages.error(request, "Cet élève a déjà 2 parents liés à son compte.")
            else:
                eleve.parents.add(request.user)
                messages.success(request, f"{eleve.prenom} {eleve.nom} est maintenant lié à votre compte.")
                return redirect("portal:dashboard")
    else:
        form = CodeParentForm()

    return render(request, "students/lier_parent.html", {"form": form})