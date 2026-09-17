from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from configuration.models import SchoolStaff
from .forms import SchoolYearForm, PeriodForm
from .models import SchoolYear, Period


@login_required
def gerer_annees(request):

    if not SchoolStaff.objects.filter(user=request.user).exists():
        messages.error(request, "Vous devez d'abord créer ou rejoindre un établissement.")
        return redirect("portal:dashboard")

    if request.method == "POST":
        form = SchoolYearForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Année scolaire créée avec succès.")
            return redirect("school:gerer_annees")
    else:
        form = SchoolYearForm()

    annees = SchoolYear.objects.all()

    return render(request, "school/gerer_annees.html", {
        "form": form,
        "annees": annees,
    })


@login_required
def modifier_annee(request, pk):

    annee = get_object_or_404(SchoolYear, pk=pk)

    if request.method == "POST":
        form = SchoolYearForm(request.POST, instance=annee)
        if form.is_valid():
            form.save()
            messages.success(request, "Année scolaire modifiée avec succès.")
            return redirect("school:gerer_annees")
    else:
        form = SchoolYearForm(instance=annee)

    return render(request, "school/modifier_annee.html", {
        "form": form,
        "annee": annee,
    })


@login_required
def activer_annee(request, pk):
    SchoolYear.objects.update(active=False)
    annee = get_object_or_404(SchoolYear, pk=pk)
    annee.active = True
    annee.save()
    messages.success(request, f"« {annee.nom} » est maintenant l'année active.")
    return redirect("school:gerer_annees")


@login_required
def gerer_periodes(request):

    if not SchoolStaff.objects.filter(user=request.user).exists():
        messages.error(request, "Vous devez d'abord créer ou rejoindre un établissement.")
        return redirect("portal:dashboard")

    if request.method == "POST":
        form = PeriodForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Période créée avec succès.")
            return redirect("school:gerer_periodes")
    else:
        form = PeriodForm()

    periodes = Period.objects.select_related("school_year").all()

    return render(request, "school/gerer_periodes.html", {
        "form": form,
        "periodes": periodes,
    })


@login_required
def modifier_periode(request, pk):

    periode = get_object_or_404(Period, pk=pk)

    if request.method == "POST":
        form = PeriodForm(request.POST, instance=periode)
        if form.is_valid():
            form.save()
            messages.success(request, "Période modifiée avec succès.")
            return redirect("school:gerer_periodes")
    else:
        form = PeriodForm(instance=periode)

    return render(request, "school/modifier_periode.html", {
        "form": form,
        "periode": periode,
    })


@login_required
def activer_periode(request, pk):
    periode = get_object_or_404(Period, pk=pk)
    Period.objects.filter(school_year=periode.school_year).update(is_active=False)
    periode.is_active = True
    periode.save()
    messages.success(request, f"« {periode.get_name_display()} » est maintenant la période active.")
    return redirect("school:gerer_periodes")