import random
from .forms import RechercheEnseignantForm, InscriptionEnseignantForm, PinForm, ProfilEnseignantForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from configuration.models import SchoolStaff, SchoolProfile
from accounts.models import CustomUser
from .forms import RechercheEnseignantForm, InscriptionEnseignantForm, PinForm
from .models import Teacher, TeacherSchoolAccess


def _generer_pin():
    return "".join(random.choices("0123456789", k=4))


@login_required
def gerer_enseignants(request):

    school_staff = SchoolStaff.objects.filter(user=request.user).select_related("school").first()

    if not school_staff:
        messages.error(request, "Vous devez d'abord créer ou rejoindre un établissement.")
        return redirect("portal:dashboard")

    school = school_staff.school

    if request.method == "POST":
        form = RechercheEnseignantForm(request.POST)
        if form.is_valid():
            identifiant = form.cleaned_data["identifiant"]

            user = CustomUser.objects.filter(username=identifiant, role="teacher").first()
            if not user:
                user = CustomUser.objects.filter(email=identifiant, role="teacher").first()

            if not user:
                messages.error(request, "Aucun enseignant trouvé avec cet identifiant.")
            else:
                teacher, _ = Teacher.objects.get_or_create(user=user)

                if TeacherSchoolAccess.objects.filter(teacher=teacher, school=school).exists():
                    messages.info(request, "Cet enseignant a déjà accès à votre établissement.")
                else:
                    pin = _generer_pin()
                    TeacherSchoolAccess.objects.create(teacher=teacher, school=school, pin_code=pin)
                    messages.success(
                        request,
                        f"{user.get_full_name() or user.username} a été ajouté. "
                        f"Code PIN à lui communiquer : {pin}"
                    )
                return redirect("teachers:gerer_enseignants")
    else:
        form = RechercheEnseignantForm()

    enseignants = TeacherSchoolAccess.objects.filter(school=school).select_related("teacher__user")

    return render(request, "teachers/gerer_enseignants.html", {
        "form": form,
        "school": school,
        "enseignants": enseignants,
    })


@login_required
def inscrire_enseignant(request):

    school_staff = SchoolStaff.objects.filter(user=request.user).select_related("school").first()

    if not school_staff:
        messages.error(request, "Vous devez d'abord créer ou rejoindre un établissement.")
        return redirect("portal:dashboard")

    school = school_staff.school

    if request.method == "POST":
        form = InscriptionEnseignantForm(request.POST, school=school)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "teacher"
            user.save()

            teacher = Teacher.objects.create(user=user)
            teacher.matieres.set(form.cleaned_data["matieres"])
            teacher.classes.set(form.cleaned_data["classes"])

            pin = _generer_pin()
            TeacherSchoolAccess.objects.create(teacher=teacher, school=school, pin_code=pin)

            messages.success(
                request,
                f"Compte créé pour {user.get_full_name() or user.username}. "
                f"Identifiant : {user.username} — Code PIN établissement : {pin} — "
                f"transmettez-lui le mot de passe et le PIN."
            )
            return redirect("teachers:gerer_enseignants")
    else:
        form = InscriptionEnseignantForm(school=school)

    return render(request, "teachers/inscrire_enseignant.html", {
        "form": form,
        "school": school,
    })


@login_required
def mes_ecoles(request):

    teacher = Teacher.objects.filter(user=request.user).first()
    if not teacher:
        messages.error(request, "Accès réservé aux enseignants.")
        return redirect("portal:dashboard")

    acces = TeacherSchoolAccess.objects.filter(teacher=teacher).select_related("school")

    return render(request, "teachers/mes_ecoles.html", {
        "acces": acces,
    })


@login_required
def entrer_ecole(request, school_id):

    teacher = Teacher.objects.filter(user=request.user).first()
    school = get_object_or_404(SchoolProfile, pk=school_id)

    acces = TeacherSchoolAccess.objects.filter(teacher=teacher, school=school).first()
    if not acces:
        messages.error(request, "Vous n'avez pas accès à cet établissement.")
        return redirect("teachers:mes_ecoles")

    if request.method == "POST":
        form = PinForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["pin_code"] == acces.pin_code:
                request.session[f"unlocked_school_{school.pk}"] = True
                return redirect("teachers:mes_classes", school_id=school.pk)
            else:
                messages.error(request, "Code PIN incorrect.")
    else:
        form = PinForm()

    return render(request, "teachers/entrer_ecole.html", {
        "form": form,
        "school": school,
    })


@login_required
def mes_classes(request, school_id):

    teacher = Teacher.objects.filter(user=request.user).first()
    school = get_object_or_404(SchoolProfile, pk=school_id)

    if not request.session.get(f"unlocked_school_{school.pk}"):
        return redirect("teachers:entrer_ecole", school_id=school.pk)

    classes = teacher.classes.filter(school=school)

    return render(request, "teachers/mes_classes.html", {
        "teacher": teacher,
        "school": school,
        "classes": classes,
    })
@login_required
def mes_coordonnees(request):

    teacher, _ = Teacher.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfilEnseignantForm(request.POST)
        if form.is_valid():
            request.user.phone = form.cleaned_data["phone"]
            request.user.save()
            teacher.adresse = form.cleaned_data["adresse"]
            teacher.bio = form.cleaned_data["bio"]
            teacher.save()
            messages.success(request, "Coordonnées enregistrées.")
            return redirect("teachers:mes_ecoles")
    else:
        form = ProfilEnseignantForm(initial={
            "phone": request.user.phone,
            "adresse": teacher.adresse,
            "bio": teacher.bio,
        })

    return render(request, "teachers/mes_coordonnees.html", {"form": form})


@login_required
def reinitialiser_pin(request, access_id):

    school_staff = SchoolStaff.objects.filter(user=request.user).select_related("school").first()
    if not school_staff:
        messages.error(request, "Accès réservé à l'administration d'un établissement.")
        return redirect("portal:dashboard")

    acces = get_object_or_404(TeacherSchoolAccess, pk=access_id, school=school_staff.school)
    nouveau_pin = _generer_pin()
    acces.pin_code = nouveau_pin
    acces.save()

    messages.success(
        request,
        f"Nouveau code PIN pour {acces.teacher.user.get_full_name() or acces.teacher.user.username} : {nouveau_pin} — "
        f"transmettez-le lui."
    )
    return redirect("teachers:gerer_enseignants")