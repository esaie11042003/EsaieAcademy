from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .forms import InscriptionForm, RechercheAdminForm, InscriptionAdminForm
from .models import CustomUser


def inscription(request):
    if request.method == "POST":
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("portal:dashboard")
    else:
        form = InscriptionForm()

    return render(request, "accounts/inscription.html", {"form": form})


def _est_super_admin(user):
    return user.is_authenticated and user.is_superuser


@user_passes_test(_est_super_admin)
def gerer_admins(request):

    if request.method == "POST":
        form = RechercheAdminForm(request.POST)
        if form.is_valid():
            identifiant = form.cleaned_data["identifiant"]

            user = CustomUser.objects.filter(username=identifiant).first()
            if not user:
                user = CustomUser.objects.filter(email=identifiant).first()

            if not user:
                messages.error(request, "Aucun compte trouvé avec cet identifiant.")
            elif user.is_superuser:
                messages.info(request, "Ce compte est déjà l'administrateur général.")
            elif user.role == "admin":
                messages.info(request, "Ce compte est déjà co-administrateur.")
            else:
                user.role = "admin"
                user.save()
                messages.success(request, f"{user.get_full_name() or user.username} est maintenant co-administrateur.")
                return redirect("accounts:gerer_admins")
    else:
        form = RechercheAdminForm()

    admins = CustomUser.objects.filter(role="admin").order_by("-is_superuser", "username")

    return render(request, "accounts/gerer_admins.html", {
        "form": form,
        "admins": admins,
    })


@user_passes_test(_est_super_admin)
def inscrire_admin(request):

    if request.method == "POST":
        form = InscriptionAdminForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "admin"
            user.save()
            messages.success(
                request,
                f"Compte administrateur créé pour {user.get_full_name() or user.username}. "
                f"Identifiant : {user.username} — transmettez-lui le mot de passe choisi."
            )
            return redirect("accounts:gerer_admins")
    else:
        form = InscriptionAdminForm()

    return render(request, "accounts/inscrire_admin.html", {"form": form})


@user_passes_test(_est_super_admin)
def retirer_admin(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)

    if user.is_superuser:
        messages.error(request, "Impossible de retirer les droits de l'administrateur général.")
        return redirect("accounts:gerer_admins")

    if user.pk == request.user.pk:
        messages.error(request, "Vous ne pouvez pas retirer vos propres droits.")
        return redirect("accounts:gerer_admins")

    user.role = "staff"
    user.save()
    messages.success(request, f"{user.get_full_name() or user.username} n'est plus co-administrateur.")
    return redirect("accounts:gerer_admins")


@user_passes_test(_est_super_admin)
def basculer_statut_admin(request, pk):
    """Active ou désactive un co-administrateur. Toi seul peux le faire."""
    user = get_object_or_404(CustomUser, pk=pk)

    if user.is_superuser:
        messages.error(request, "Impossible de désactiver l'administrateur général.")
        return redirect("accounts:gerer_admins")

    if user.pk == request.user.pk:
        messages.error(request, "Vous ne pouvez pas vous désactiver vous-même.")
        return redirect("accounts:gerer_admins")

    user.is_active = not user.is_active
    user.save()

    if user.is_active:
        messages.success(request, f"{user.get_full_name() or user.username} a été réactivé.")
    else:
        messages.success(request, f"{user.get_full_name() or user.username} a été désactivé — il ne peut plus se connecter.")

    return redirect("accounts:gerer_admins")


@user_passes_test(_est_super_admin)
def supprimer_admin(request, pk):
    """Supprime définitivement un co-administrateur. Toi seul peux le faire."""
    user = get_object_or_404(CustomUser, pk=pk)

    if user.is_superuser:
        messages.error(request, "Impossible de supprimer l'administrateur général.")
        return redirect("accounts:gerer_admins")

    if user.pk == request.user.pk:
        messages.error(request, "Vous ne pouvez pas vous supprimer vous-même.")
        return redirect("accounts:gerer_admins")

    if request.method == "POST":
        nom = user.get_full_name() or user.username
        user.delete()
        messages.success(request, f"Le compte de {nom} a été supprimé définitivement.")
        return redirect("accounts:gerer_admins")

    return render(request, "accounts/supprimer_admin.html", {"admin_cible": user})
