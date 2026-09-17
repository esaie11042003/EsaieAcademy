from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from configuration.models import SchoolStaff
from .forms import ClasseForm
from .models import Classe


@login_required
def creer_classe(request):

    school_staff = SchoolStaff.objects.filter(user=request.user).select_related("school").first()
    school = school_staff.school if school_staff else None

    if not school_staff and request.user.role != "admin":
        messages.error(request, "Vous devez d'abord créer ou rejoindre un établissement.")
        return redirect("portal:dashboard")

    if request.method == "POST":
        form = ClasseForm(request.POST, school=school)
        if form.is_valid():
            classe = form.save(commit=False)
            classe.school = school
            classe.save()
            form.save_m2m()
            messages.success(request, f"Classe « {classe.nom} » créée avec succès.")
            return redirect("classes:creer_classe")
    else:
        form = ClasseForm(school=school)

    if school:
        classes = Classe.objects.filter(school=school)
    else:
        classes = Classe.objects.filter(school__isnull=True)

    return render(request, "classes/creer_classe.html", {
        "form": form,
        "school": school,
        "classes": classes,
    })


@login_required
def modifier_classe(request, pk):

    classe = get_object_or_404(Classe, pk=pk)

    if request.method == "POST":
        form = ClasseForm(request.POST, instance=classe, school=classe.school)
        if form.is_valid():
            form.save()
            messages.success(request, f"Classe « {classe.nom} » modifiée avec succès.")
            return redirect("classes:creer_classe")
    else:
        form = ClasseForm(instance=classe, school=classe.school)

    return render(request, "classes/modifier_classe.html", {
        "form": form,
        "classe": classe,
    })