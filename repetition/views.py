from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DemandeMaitreEtude, MessageDemande
from .forms import DemandeMaitreEtudeForm, MessageDemandeForm, RdvForm, SuiviForm


def deposer_demande(request):
    """Formulaire public — accessible sans connexion (visiteurs, élèves, parents)."""

    if request.method == "POST":
        form = DemandeMaitreEtudeForm(request.POST)
        if form.is_valid():
            demande = form.save(commit=False)
            if request.user.is_authenticated:
                demande.demandeur = request.user
            demande.save()
            request.session["dernier_code_suivi"] = demande.code_suivi
            messages.success(request, "Votre demande a bien été envoyée.")
            return redirect("repetition:merci")
    else:
        form = DemandeMaitreEtudeForm()

    return render(request, "repetition/deposer_demande.html", {"form": form})


def merci(request):
    code = request.session.pop("dernier_code_suivi", None)
    return render(request, "repetition/merci.html", {"code_suivi": code})


def _admin_autorise(request):
    return request.user.is_authenticated and (request.user.is_superuser or request.user.role == "admin")


@login_required
def liste_demandes(request):

    if not _admin_autorise(request):
        messages.error(request, "Accès réservé aux administrateurs de la plateforme.")
        return redirect("portal:dashboard")

    demandes = DemandeMaitreEtude.objects.all()

    return render(request, "repetition/liste_demandes.html", {"demandes": demandes})


@login_required
def detail_demande(request, pk):
    """Vue ADMIN : répondre, planifier le rendez-vous, changer le statut."""

    if not _admin_autorise(request):
        messages.error(request, "Accès réservé aux administrateurs de la plateforme.")
        return redirect("portal:dashboard")

    demande = get_object_or_404(DemandeMaitreEtude, pk=pk)
    message_form = MessageDemandeForm()
    rdv_form = RdvForm(instance=demande)

    if request.method == "POST":
        if "envoyer_message" in request.POST:
            message_form = MessageDemandeForm(request.POST)
            if message_form.is_valid():
                msg = message_form.save(commit=False)
                msg.demande = demande
                msg.auteur = request.user
                msg.is_admin = True
                msg.save()
                if demande.statut == "nouvelle":
                    demande.statut = "en_discussion"
                    demande.traite_par = request.user
                    demande.save()
                messages.success(request, "Message envoyé.")
                return redirect("repetition:detail_demande", pk=demande.pk)

        elif "planifier_rdv" in request.POST:
            rdv_form = RdvForm(request.POST, instance=demande)
            if rdv_form.is_valid():
                rdv_form.save()
                messages.success(request, "Rendez-vous mis à jour.")
                return redirect("repetition:detail_demande", pk=demande.pk)

    return render(request, "repetition/detail_demande.html", {
        "demande": demande,
        "message_form": message_form,
        "rdv_form": rdv_form,
    })


@login_required
def mes_demandes(request):
    """Pour un utilisateur connecté (élève, parent, visiteur inscrit) :
    la liste de ses propres demandes."""

    demandes = DemandeMaitreEtude.objects.filter(demandeur=request.user)

    return render(request, "repetition/mes_demandes.html", {"demandes": demandes})


def _peut_voir_demande(request, demande):
    if request.user.is_authenticated and demande.demandeur_id == request.user.id:
        return True
    if request.session.get("demandes_suivies") and demande.pk in request.session["demandes_suivies"]:
        return True
    return False


@login_required
def suivre_fil_utilisateur(request, pk):
    """Vue UTILISATEUR CONNECTÉ : voir le fil et répondre à sa propre demande."""

    demande = get_object_or_404(DemandeMaitreEtude, pk=pk)

    if not _peut_voir_demande(request, demande):
        messages.error(request, "Vous n'êtes pas autorisé à voir cette demande.")
        return redirect("portal:dashboard")

    if request.method == "POST":
        message_form = MessageDemandeForm(request.POST)
        if message_form.is_valid():
            msg = message_form.save(commit=False)
            msg.demande = demande
            msg.auteur = request.user if request.user.is_authenticated else None
            msg.is_admin = False
            msg.save()
            messages.success(request, "Message envoyé.")
            return redirect("repetition:suivre_fil_utilisateur", pk=demande.pk)
    else:
        message_form = MessageDemandeForm()

    return render(request, "repetition/detail_demande_utilisateur.html", {
        "demande": demande,
        "message_form": message_form,
    })


def suivre_demande(request):
    """
    Page PUBLIQUE (pas besoin de compte) : retrouver une demande
    avec le téléphone + le code de suivi, voir le fil et répondre.
    """

    demande = None

    if request.method == "POST" and "verifier_code" in request.POST:
        form = SuiviForm(request.POST)
        if form.is_valid():
            demande = DemandeMaitreEtude.objects.filter(
                telephone_contact=form.cleaned_data["telephone"],
                code_suivi=form.cleaned_data["code_suivi"],
            ).first()
            if demande:
                suivies = request.session.get("demandes_suivies", [])
                if demande.pk not in suivies:
                    suivies.append(demande.pk)
                request.session["demandes_suivies"] = suivies
            else:
                messages.error(request, "Aucune demande ne correspond à ces informations.")
    else:
        form = SuiviForm()

    if request.method == "POST" and "envoyer_message" in request.POST:
        demande_pk = request.POST.get("demande_pk")
        suivies = request.session.get("demandes_suivies", [])
        if int(demande_pk) in suivies:
            demande = get_object_or_404(DemandeMaitreEtude, pk=demande_pk)
            message_form = MessageDemandeForm(request.POST)
            if message_form.is_valid():
                msg = message_form.save(commit=False)
                msg.demande = demande
                msg.is_admin = False
                msg.save()
                messages.success(request, "Message envoyé.")

    message_form = MessageDemandeForm()

    return render(request, "repetition/suivre_demande.html", {
        "form": form,
        "demande": demande,
        "message_form": message_form,
    })