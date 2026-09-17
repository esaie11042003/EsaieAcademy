from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import InscriptionForm
from django.contrib.auth.decorators import user_passes_test
from .forms import RechercheAdminForm, InscriptionAdminForm
from django.shortcuts import get_object_or_404


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
    return user.is_superuser


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
            elif user.role == "admin":
                messages.info(request, "Ce compte est déjà administrateur.")
            else:
                user.role = "admin"
                user.save()
                messages.success(request, f"{user.get_full_name() or user.username} est maintenant co-administrateur.")
                return redirect("accounts:gerer_admins")
    else:
        form = RechercheAdminForm()

    admins = CustomUser.objects.filter(role="admin")

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
        messages.error(request, "Impossible de retirer l'administrateur général.")
        return redirect("accounts:gerer_admins")

    user.role = "staff"
    user.save()
    messages.success(request, f"{user.get_full_name() or user.username} n'est plus co-administrateur.")
    return redirect("accounts:gerer_admins")