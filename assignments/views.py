from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from configuration.models import SchoolStaff
from .forms import AssignmentForm
from .models import Assignment


@login_required
def gerer_affectations(request):

    school_staff = SchoolStaff.objects.filter(user=request.user).select_related("school").first()

    if not school_staff:
        messages.error(request, "Vous devez d'abord créer ou rejoindre un établissement.")
        return redirect("portal:dashboard")

    school = school_staff.school

    if request.method == "POST":
        form = AssignmentForm(request.POST, school=school)
        if form.is_valid():
            form.save()
            messages.success(request, "Affectation créée avec succès.")
            return redirect("assignments:gerer_affectations")
    else:
        form = AssignmentForm(school=school)

    affectations = Assignment.objects.filter(classe__school=school).select_related(
        "teacher__user", "classe", "subject", "school_year"
    )

    return render(request, "assignments/gerer_affectations.html", {
        "form": form,
        "school": school,
        "affectations": affectations,
    })