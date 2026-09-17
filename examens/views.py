from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from datetime import timedelta

from .forms import EpreuveExamenForm, ExamenForm
from .models import Examen, EpreuveExamen


def _a_acces(user, epreuve):
    if not epreuve.is_payant or not epreuve.prix:
        return True
    if user.is_authenticated and user.role == "admin":
        return True
    if not user.is_authenticated:
        return False
    from monetisation.models import Purchase
    ct = ContentType.objects.get_for_model(epreuve)
    return Purchase.objects.filter(
        content_type=ct, object_id=epreuve.pk, acheteur=user, statut="VALIDE"
    ).exists()


def liste_examens(request):
    query = request.GET.get("q", "").strip()

    if request.user.is_authenticated and request.user.role == "admin":
        base_qs = EpreuveExamen.objects.filter(is_deleted=False)
    else:
        base_qs = EpreuveExamen.objects.filter(is_active=True, is_deleted=False)

    if query:
        epreuves = base_qs.filter(
            Q(titre__icontains=query) |
            Q(examen__nom__icontains=query) |
            Q(annee__icontains=query)
        ).select_related("examen")
        for e in epreuves:
            e.a_acces = _a_acces(request.user, e)
        examens_list = None
    else:
        epreuves = None
        examens_list = Examen.objects.all()
        for ex in examens_list:
            ex.epreuves_visibles = base_qs.filter(examen=ex)
            for e in ex.epreuves_visibles:
                e.a_acces = _a_acces(request.user, e)

    return render(request, "examens/liste.html", {
        "examens_list": examens_list,
        "epreuves": epreuves,
        "query": query,
    })


@login_required
def ajouter_epreuve(request):

    if request.user.role not in ("staff", "admin"):
        messages.error(request, "Accès réservé au personnel administratif.")
        return redirect("examens:liste_examens")

    if request.method == "POST":
        form = EpreuveExamenForm(request.POST, request.FILES)
        if form.is_valid():
            epreuve = form.save(commit=False)
            epreuve.ajoute_par = request.user
            epreuve.save()
            messages.success(request, "Épreuve ajoutée avec succès.")
            return redirect("examens:liste_examens")
    else:
        form = EpreuveExamenForm()

    return render(request, "examens/ajouter_epreuve.html", {"form": form})


@login_required
def gerer_examens(request):

    if request.user.role != "admin":
        messages.error(request, "Accès réservé aux administrateurs de la plateforme.")
        return redirect("examens:liste_examens")

    if request.method == "POST":
        form = ExamenForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Examen créé avec succès.")
            return redirect("examens:gerer_examens")
    else:
        form = ExamenForm()

    examens_list = Examen.objects.all()

    return render(request, "examens/gerer_examens.html", {
        "form": form,
        "examens_list": examens_list,
    })


@login_required
def modifier_epreuve(request, pk):

    epreuve = get_object_or_404(EpreuveExamen, pk=pk)

    if request.user.role != "admin":
        messages.error(request, "Accès réservé aux administrateurs de la plateforme.")
        return redirect("examens:liste_examens")

    if request.method == "POST":
        epreuve.examen_id = request.POST.get("examen") or epreuve.examen_id
        epreuve.titre = request.POST.get("titre", epreuve.titre)
        epreuve.annee = request.POST.get("annee", epreuve.annee)
        epreuve.is_payant = request.POST.get("is_payant") == "on"
        epreuve.prix = request.POST.get("prix") or None
        epreuve.save()
        messages.success(request, "Épreuve mise à jour avec succès.")
        return redirect("examens:liste_examens")

    examens_list = Examen.objects.all()

    return render(request, "examens/modifier_epreuve.html", {
        "epreuve": epreuve,
        "examens_list": examens_list,
    })


@login_required
def basculer_epreuve(request, pk):

    if request.user.role != "admin":
        messages.error(request, "Accès réservé aux administrateurs de la plateforme.")
        return redirect("examens:liste_examens")

    epreuve = get_object_or_404(EpreuveExamen, pk=pk)
    epreuve.is_active = not epreuve.is_active
    epreuve.save()

    if epreuve.is_active:
        messages.success(request, f"« {epreuve.titre} » est de nouveau visible.")
    else:
        messages.success(request, f"« {epreuve.titre} » a été désactivée — visible uniquement par les admins.")

    return redirect("examens:liste_examens")


@login_required
def supprimer_epreuve(request, pk):

    if request.user.role != "admin":
        messages.error(request, "Accès réservé aux administrateurs de la plateforme.")
        return redirect("examens:liste_examens")

    epreuve = get_object_or_404(EpreuveExamen, pk=pk)

    if request.method == "POST":
        epreuve.is_deleted = True
        epreuve.deleted_at = timezone.now()
        epreuve.is_active = False
        epreuve.save()
        messages.success(request, f"« {epreuve.titre} » a été déplacée vers la corbeille (suppression définitive dans 30 jours).")
        return redirect("examens:liste_examens")

    return render(request, "examens/supprimer_epreuve.html", {"epreuve": epreuve})


@login_required
def corbeille_examens(request):

    if request.user.role != "admin":
        messages.error(request, "Accès réservé aux administrateurs de la plateforme.")
        return redirect("examens:liste_examens")

    limite = timezone.now() - timedelta(days=30)
    EpreuveExamen.objects.filter(is_deleted=True, deleted_at__lt=limite).delete()

    epreuves = EpreuveExamen.objects.filter(is_deleted=True).select_related("examen")
    for e in epreuves:
        jours_restants = 30 - (timezone.now() - e.deleted_at).days
        e.jours_restants = max(jours_restants, 0)

    return render(request, "examens/corbeille.html", {"epreuves": epreuves})


@login_required
def restaurer_epreuve(request, pk):

    if request.user.role != "admin":
        messages.error(request, "Accès réservé aux administrateurs de la plateforme.")
        return redirect("examens:liste_examens")

    epreuve = get_object_or_404(EpreuveExamen, pk=pk, is_deleted=True)
    epreuve.is_deleted = False
    epreuve.deleted_at = None
    epreuve.save()
    messages.success(request, f"« {epreuve.titre} » a été restaurée.")
    return redirect("examens:corbeille_examens")


@login_required
def supprimer_definitivement_epreuve(request, pk):

    if request.user.role != "admin":
        messages.error(request, "Accès réservé aux administrateurs de la plateforme.")
        return redirect("examens:liste_examens")

    epreuve = get_object_or_404(EpreuveExamen, pk=pk, is_deleted=True)
    titre = epreuve.titre
    epreuve.delete()
    messages.success(request, f"« {titre} » a été supprimée définitivement.")
    return redirect("examens:corbeille_examens")


@login_required
def epreuves_desactivees(request):

    if request.user.role != "admin":
        messages.error(request, "Accès réservé aux administrateurs de la plateforme.")
        return redirect("examens:liste_examens")

    epreuves = EpreuveExamen.objects.filter(is_active=False, is_deleted=False).select_related("examen")

    return render(request, "examens/epreuves_desactivees.html", {"epreuves": epreuves})


@login_required
def telecharger(request, pk, type_fichier):
    epreuve = get_object_or_404(EpreuveExamen, pk=pk)

    if not _a_acces(request.user, epreuve):
        messages.error(request, "Vous devez payer cette épreuve pour y accéder.")
        ct = ContentType.objects.get_for_model(epreuve)
        return redirect("monetisation:acheter", app_label=ct.app_label, model_name=ct.model, pk=epreuve.pk)

    if type_fichier == "sujet":
        return redirect(epreuve.fichier_sujet.url)
    return redirect(epreuve.fichier_corrige.url)