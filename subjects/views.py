from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from configuration.models import SchoolStaff
from .forms import SubjectForm
from .models import Subject


@login_required
def gerer_matieres(request):

    est_staff = SchoolStaff.objects.filter(user=request.user).exists()
    if not est_staff and request.user.role != "admin":
        messages.error(request, "Vous devez d'abord créer ou rejoindre un établissement.")
        return redirect("portal:dashboard")
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Matière créée avec succès.")
            return redirect("subjects:gerer_matieres")
    else:
        form = SubjectForm()

    matieres = Subject.objects.all()

    return render(request, "subjects/gerer_matieres.html", {
        "form": form,
        "matieres": matieres,
    })


@login_required
def modifier_matiere(request, pk):

    matiere = get_object_or_404(Subject, pk=pk)

    if request.method == "POST":
        form = SubjectForm(request.POST, instance=matiere)
        if form.is_valid():
            form.save()
            messages.success(request, f"Matière « {matiere.nom} » modifiée avec succès.")
            return redirect("subjects:gerer_matieres")
    else:
        form = SubjectForm(instance=matiere)

    return render(request, "subjects/modifier_matiere.html", {
        "form": form,
        "matiere": matiere,
    })