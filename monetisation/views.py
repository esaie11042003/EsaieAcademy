import random
import string

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from .models import ReceivingAccount, Purchase
from .forms import ReceivingAccountForm


def _generer_reference():
    caracteres = string.ascii_uppercase + string.digits
    return "EA-" + "".join(random.choices(caracteres, k=8))


@login_required
def gerer_comptes_reception(request):

    if request.user.role != "admin":
        messages.error(request, "Accès réservé aux administrateurs de la plateforme.")
        return redirect("portal:dashboard")

    for code, _ in ReceivingAccount.OPERATEUR_CHOICES:
        ReceivingAccount.objects.get_or_create(operateur=code, defaults={"numero": ""})

    if request.method == "POST":
        compte_id = request.POST.get("compte_id")
        compte = get_object_or_404(ReceivingAccount, pk=compte_id)
        compte.numero = request.POST.get("numero", "").strip()
        compte.actif = request.POST.get("actif") == "on"
        compte.note = request.POST.get("note", "").strip()
        compte.save()
        messages.success(request, f"Numéro {compte.get_operateur_display()} mis à jour.")
        return redirect("monetisation:gerer_comptes_reception")

    comptes = ReceivingAccount.objects.all().order_by("operateur")

    return render(request, "monetisation/gerer_comptes_reception.html", {
        "comptes": comptes,
    })


@login_required
def acheter(request, app_label, model_name, pk):

    ct = get_object_or_404(ContentType, app_label=app_label, model=model_name)
    resource = get_object_or_404(ct.model_class(), pk=pk)

    prix = getattr(resource, "prix", None)
    if not prix:
        messages.error(request, "Cette ressource n'est pas payante.")
        return redirect("portal:dashboard")

    achat = Purchase.objects.filter(
        content_type=ct, object_id=resource.pk, acheteur=request.user, statut="EN_ATTENTE"
    ).first()

    comptes_actifs = ReceivingAccount.objects.filter(actif=True).exclude(numero="")

    if request.method == "POST" and not achat:
        operateur = request.POST.get("operateur")
        compte = comptes_actifs.filter(operateur=operateur).first()
        if not compte:
            messages.error(request, "Ce numéro n'est pas disponible actuellement.")
        else:
            achat = Purchase.objects.create(
                content_type=ct,
                object_id=resource.pk,
                acheteur=request.user,
                operateur=operateur,
                numero_reception=compte.numero,
                montant=prix,
                reference_paiement=_generer_reference(),
            )
            return redirect("monetisation:acheter", app_label=app_label, model_name=model_name, pk=pk)

    return render(request, "monetisation/acheter.html", {
        "resource": resource,
        "prix": prix,
        "comptes_actifs": comptes_actifs,
        "achat": achat,
    })


@login_required
def mes_achats(request):
    achats = Purchase.objects.filter(acheteur=request.user).select_related("content_type")
    return render(request, "monetisation/mes_achats.html", {"achats": achats})


@login_required
def espace_paiements(request):

    if request.user.role != "admin":
        messages.error(request, "Accès réservé aux administrateurs de la plateforme.")
        return redirect("portal:dashboard")

    statut = request.GET.get("statut", "EN_ATTENTE")

    achats = Purchase.objects.filter(statut=statut).select_related("acheteur", "content_type")

    context = {
        "achats": achats,
        "statut": statut,
        "nb_en_attente": Purchase.objects.filter(statut="EN_ATTENTE").count(),
        "nb_valides": Purchase.objects.filter(statut="VALIDE").count(),
        "nb_rejetes": Purchase.objects.filter(statut="REJETE").count(),
    }

    return render(request, "monetisation/espace_paiements.html", context)


@login_required
def valider_achat(request, pk):

    if request.user.role != "admin":
        messages.error(request, "Accès réservé aux administrateurs de la plateforme.")
        return redirect("portal:dashboard")

    achat = get_object_or_404(Purchase, pk=pk)
    achat.statut = "VALIDE"
    achat.validated_by = request.user
    achat.validated_at = timezone.now()
    achat.save()

    messages.success(request, f"Achat de {achat.acheteur} validé — accès débloqué.")
    return redirect("monetisation:espace_paiements")


@login_required
def rejeter_achat(request, pk):

    if request.user.role != "admin":
        messages.error(request, "Accès réservé aux administrateurs de la plateforme.")
        return redirect("portal:dashboard")

    achat = get_object_or_404(Purchase, pk=pk)
    achat.statut = "REJETE"
    achat.validated_by = request.user
    achat.validated_at = timezone.now()
    achat.save()

    messages.success(request, f"Achat de {achat.acheteur} rejeté.")
    return redirect("monetisation:espace_paiements")


@login_required
def recu(request, pk):
    achat = get_object_or_404(Purchase, pk=pk, acheteur=request.user, statut="VALIDE")
    return render(request, "monetisation/recu.html", {"achat": achat})
@login_required
def annuler_achat(request, pk):
    achat = get_object_or_404(Purchase, pk=pk, acheteur=request.user, statut="EN_ATTENTE")
    ct = achat.content_type
    resource_pk = achat.object_id
    achat.delete()
    return redirect("monetisation:acheter", app_label=ct.app_label, model_name=ct.model, pk=resource_pk)