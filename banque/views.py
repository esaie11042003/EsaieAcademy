from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from datetime import timedelta

from .forms import EpreuveClasseForm, DocumentClasseForm
from .models import EpreuveClasse, DocumentClasse
from classes.models import Classe


def _a_acces(user, item):
    if not item.is_payant or not item.prix:
        return True
    if user.is_authenticated and user.role == "admin":
        return True
    if not user.is_authenticated:
        return False
    from monetisation.models import Purchase
    ct = ContentType.objects.get_for_model(item)
    return Purchase.objects.filter(content_type=ct, object_id=item.pk, acheteur=user, statut="VALIDE").exists()


# ============ ÉPREUVES ============

def liste_epreuves(request):
    query = request.GET.get("q", "").strip()

    if request.user.is_authenticated and request.user.role == "admin":
        base_qs = EpreuveClasse.objects.filter(is_deleted=False)
    else:
        base_qs = EpreuveClasse.objects.filter(is_active=True, is_deleted=False)

    if query:
        epreuves = base_qs.filter(Q(titre__icontains=query) | Q(classe__nom__icontains=query) | Q(annee__icontains=query)).select_related("classe")
        for e in epreuves:
            e.a_acces = _a_acces(request.user, e)
        classes_list = None
    else:
        epreuves = None
        classes_list = Classe.objects.all()
        for c in classes_list:
            c.epreuves_visibles = base_qs.filter(classe=c)
            for e in c.epreuves_visibles:
                e.a_acces = _a_acces(request.user, e)

    return render(request, "banque/liste_epreuves.html", {"classes_list": classes_list, "epreuves": epreuves, "query": query})


@login_required
def ajouter_epreuve(request):
    if request.user.role not in ("staff", "admin"):
        messages.error(request, "Accès réservé au personnel administratif.")
        return redirect("banque:liste_epreuves")

    if request.method == "POST":
        form = EpreuveClasseForm(request.POST, request.FILES)
        if form.is_valid():
            e = form.save(commit=False)
            e.ajoute_par = request.user
            e.save()
            messages.success(request, "Épreuve ajoutée avec succès.")
            return redirect("banque:liste_epreuves")
    else:
        form = EpreuveClasseForm()

    return render(request, "banque/ajouter_epreuve.html", {"form": form})


@login_required
def modifier_epreuve(request, pk):
    e = get_object_or_404(EpreuveClasse, pk=pk)
    if request.user.role != "admin":
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect("banque:liste_epreuves")

    if request.method == "POST":
        e.classe_id = request.POST.get("classe") or e.classe_id
        e.titre = request.POST.get("titre", e.titre)
        e.annee = request.POST.get("annee", e.annee)
        e.is_payant = request.POST.get("is_payant") == "on"
        e.prix = request.POST.get("prix") or None

        if request.FILES.get("fichier_sujet"):
            if e.fichier_sujet:
                e.fichier_sujet.delete(save=False)
            e.fichier_sujet = request.FILES["fichier_sujet"]
        if request.FILES.get("fichier_corrige"):
            if e.fichier_corrige:
                e.fichier_corrige.delete(save=False)
            e.fichier_corrige = request.FILES["fichier_corrige"]

        e.save()
        messages.success(request, "Épreuve mise à jour.")
        return redirect("banque:liste_epreuves")

    return render(request, "banque/modifier_epreuve.html", {"epreuve": e, "classes_list": Classe.objects.all()})


@login_required
@require_POST
def basculer_epreuve(request, pk):
    if request.user.role != "admin":
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect("banque:liste_epreuves")
    e = get_object_or_404(EpreuveClasse, pk=pk)
    e.is_active = not e.is_active
    e.save()
    messages.success(request, "Statut mis à jour.")
    return redirect("banque:liste_epreuves")


@login_required
def supprimer_epreuve(request, pk):
    if request.user.role != "admin":
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect("banque:liste_epreuves")
    e = get_object_or_404(EpreuveClasse, pk=pk)
    if request.method == "POST":
        e.is_deleted = True
        e.deleted_at = timezone.now()
        e.is_active = False
        e.save()
        messages.success(request, "Déplacée vers la corbeille.")
        return redirect("banque:liste_epreuves")
    return render(request, "banque/supprimer_epreuve.html", {"epreuve": e})


@login_required
def corbeille_epreuves(request):
    if request.user.role != "admin":
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect("banque:liste_epreuves")
    limite = timezone.now() - timedelta(days=30)
    EpreuveClasse.objects.filter(is_deleted=True, deleted_at__lt=limite).delete()
    epreuves = EpreuveClasse.objects.filter(is_deleted=True).select_related("classe")
    for e in epreuves:
        e.jours_restants = max(30 - (timezone.now() - e.deleted_at).days, 0)
    return render(request, "banque/corbeille_epreuves.html", {"epreuves": epreuves})


@login_required
@require_POST
def restaurer_epreuve(request, pk):
    if request.user.role != "admin":
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect("banque:liste_epreuves")
    e = get_object_or_404(EpreuveClasse, pk=pk, is_deleted=True)
    e.is_deleted = False
    e.deleted_at = None
    e.save()
    messages.success(request, "Restaurée.")
    return redirect("banque:corbeille_epreuves")


@login_required
def supprimer_definitivement_epreuve(request, pk):
    if request.user.role != "admin":
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect("banque:liste_epreuves")
    e = get_object_or_404(EpreuveClasse, pk=pk, is_deleted=True)
    if request.method == "POST":
        e.delete()
        messages.success(request, "Supprimée définitivement.")
        return redirect("banque:corbeille_epreuves")
    return render(request, "banque/supprimer_definitivement_epreuve.html", {"epreuve": e})


@login_required
def epreuves_desactivees(request):
    if request.user.role != "admin":
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect("banque:liste_epreuves")
    epreuves = EpreuveClasse.objects.filter(is_active=False, is_deleted=False).select_related("classe")
    return render(request, "banque/epreuves_desactivees.html", {"epreuves": epreuves})


@login_required
def telecharger_epreuve(request, pk, type_fichier):
    e = get_object_or_404(EpreuveClasse, pk=pk)
    if not _a_acces(request.user, e):
        messages.error(request, "Vous devez payer cette épreuve pour y accéder.")
        ct = ContentType.objects.get_for_model(e)
        return redirect("monetisation:acheter", app_label=ct.app_label, model_name=ct.model, pk=e.pk)
    return redirect(e.fichier_sujet.url if type_fichier == "sujet" else e.fichier_corrige.url)


# ============ DOCUMENTS ============

def liste_documents_classe(request):
    query = request.GET.get("q", "").strip()

    if request.user.is_authenticated and request.user.role == "admin":
        base_qs = DocumentClasse.objects.filter(is_deleted=False)
    else:
        base_qs = DocumentClasse.objects.filter(is_active=True, is_deleted=False)

    if query:
        docs = base_qs.filter(Q(titre__icontains=query) | Q(classe__nom__icontains=query) | Q(annee__icontains=query)).select_related("classe")
        for d in docs:
            d.a_acces = _a_acces(request.user, d)
        classes_list = None
    else:
        docs = None
        classes_list = Classe.objects.all()
        for c in classes_list:
            c.documents_visibles = base_qs.filter(classe=c)
            for d in c.documents_visibles:
                d.a_acces = _a_acces(request.user, d)

    return render(request, "banque/liste_documents.html", {"classes_list": classes_list, "documents": docs, "query": query})


@login_required
def ajouter_document_classe(request):
    if request.user.role not in ("staff", "admin"):
        messages.error(request, "Accès réservé au personnel administratif.")
        return redirect("banque:liste_documents_classe")

    if request.method == "POST":
        form = DocumentClasseForm(request.POST, request.FILES)
        if form.is_valid():
            d = form.save(commit=False)
            d.ajoute_par = request.user
            d.save()
            messages.success(request, "Document ajouté avec succès.")
            return redirect("banque:liste_documents_classe")
    else:
        form = DocumentClasseForm()

    return render(request, "banque/ajouter_document.html", {"form": form})


@login_required
def modifier_document_classe(request, pk):
    d = get_object_or_404(DocumentClasse, pk=pk)
    if request.user.role != "admin":
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect("banque:liste_documents_classe")

    if request.method == "POST":
        d.classe_id = request.POST.get("classe") or d.classe_id
        d.titre = request.POST.get("titre", d.titre)
        d.annee = request.POST.get("annee", d.annee)
        d.is_payant = request.POST.get("is_payant") == "on"
        d.prix = request.POST.get("prix") or None

        if request.FILES.get("fichier"):
            if d.fichier:
                d.fichier.delete(save=False)
            d.fichier = request.FILES["fichier"]

        d.save()
        messages.success(request, "Document mis à jour.")
        return redirect("banque:liste_documents_classe")

    return render(request, "banque/modifier_document.html", {"document": d, "classes_list": Classe.objects.all()})


@login_required
@require_POST
def basculer_document_classe(request, pk):
    if request.user.role != "admin":
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect("banque:liste_documents_classe")
    d = get_object_or_404(DocumentClasse, pk=pk)
    d.is_active = not d.is_active
    d.save()
    messages.success(request, "Statut mis à jour.")
    return redirect("banque:liste_documents_classe")


@login_required
def supprimer_document_classe(request, pk):
    if request.user.role != "admin":
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect("banque:liste_documents_classe")
    d = get_object_or_404(DocumentClasse, pk=pk)
    if request.method == "POST":
        d.is_deleted = True
        d.deleted_at = timezone.now()
        d.is_active = False
        d.save()
        messages.success(request, "Déplacé vers la corbeille.")
        return redirect("banque:liste_documents_classe")
    return render(request, "banque/supprimer_document.html", {"document": d})


@login_required
def corbeille_documents_classe(request):
    if request.user.role != "admin":
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect("banque:liste_documents_classe")
    limite = timezone.now() - timedelta(days=30)
    DocumentClasse.objects.filter(is_deleted=True, deleted_at__lt=limite).delete()
    docs = DocumentClasse.objects.filter(is_deleted=True).select_related("classe")
    for d in docs:
        d.jours_restants = max(30 - (timezone.now() - d.deleted_at).days, 0)
    return render(request, "banque/corbeille_documents.html", {"documents": docs})


@login_required
@require_POST
def restaurer_document_classe(request, pk):
    if request.user.role != "admin":
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect("banque:liste_documents_classe")
    d = get_object_or_404(DocumentClasse, pk=pk, is_deleted=True)
    d.is_deleted = False
    d.deleted_at = None
    d.save()
    messages.success(request, "Restauré.")
    return redirect("banque:corbeille_documents_classe")


@login_required
def supprimer_definitivement_document_classe(request, pk):
    if request.user.role != "admin":
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect("banque:liste_documents_classe")
    d = get_object_or_404(DocumentClasse, pk=pk, is_deleted=True)
    if request.method == "POST":
        d.delete()
        messages.success(request, "Supprimé définitivement.")
        return redirect("banque:corbeille_documents_classe")
    return render(request, "banque/supprimer_definitivement_document_classe.html", {"document": d})


@login_required
def documents_classe_desactives(request):
    if request.user.role != "admin":
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect("banque:liste_documents_classe")
    docs = DocumentClasse.objects.filter(is_active=False, is_deleted=False).select_related("classe")
    return render(request, "banque/documents_desactives.html", {"documents": docs})


@login_required
def telecharger_document_classe(request, pk):
    d = get_object_or_404(DocumentClasse, pk=pk)
    if not _a_acces(request.user, d):
        messages.error(request, "Vous devez payer ce document pour y accéder.")
        ct = ContentType.objects.get_for_model(d)
        return redirect("monetisation:acheter", app_label=ct.app_label, model_name=ct.model, pk=d.pk)
    return redirect(d.fichier.url)