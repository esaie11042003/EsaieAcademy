from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from accounts.models import CustomUser
from students.models import Eleve
from teachers.models import TeacherSchoolAccess
from configuration.models import SchoolStaff

from .models import Forum, ForumMessage
from .forms import ForumForm, ForumMessageForm, AjoutMembreForm, AjoutParCritereForm


def _est_admin(user):
    return user.is_authenticated and (user.is_superuser or user.role == "admin")


@login_required
def mes_forums(request):
    forums = request.user.forums.filter(actif=True)
    return render(request, "forum/mes_forums.html", {"forums": forums})


@login_required
def forum_detail(request, pk):
    forum = get_object_or_404(Forum, pk=pk)

    autorise = forum.participants.filter(pk=request.user.pk).exists() or _est_admin(request.user)
    if not autorise:
        messages.error(request, "Vous n'êtes pas membre de ce forum.")
        return redirect("forum:mes_forums")

    if request.method == "POST":
        form = ForumMessageForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data["contenu"] or form.cleaned_data["fichier"]:
                msg = form.save(commit=False)
                msg.forum = forum
                msg.auteur = request.user
                msg.save()
            return redirect("forum:forum_detail", pk=pk)
    else:
        form = ForumMessageForm()

    liste_messages = forum.messages.select_related("auteur")

    return render(request, "forum/forum_detail.html", {
        "forum": forum,
        "messages_liste": liste_messages,
        "form": form,
    })


@login_required
def rejoindre_forum(request, token):
    forum = get_object_or_404(Forum, token_invitation=token, actif=True)
    forum.participants.add(request.user)
    messages.success(request, f"Vous avez rejoint le forum « {forum.nom} ».")
    return redirect("forum:forum_detail", pk=forum.pk)


@user_passes_test(_est_admin)
def liste_forums(request):
    forums = Forum.objects.all()
    return render(request, "forum/liste_forums.html", {"forums": forums})


@user_passes_test(_est_admin)
def creer_forum(request):
    if request.method == "POST":
        form = ForumForm(request.POST)
        if form.is_valid():
            forum = form.save(commit=False)
            forum.cree_par = request.user
            forum.save()
            messages.success(request, f"Forum « {forum.nom} » créé. Ajoute maintenant des membres.")
            return redirect("forum:gerer_membres", pk=forum.pk)
    else:
        form = ForumForm()

    return render(request, "forum/creer_forum.html", {"form": form})


@user_passes_test(_est_admin)
def modifier_forum(request, pk):
    forum = get_object_or_404(Forum, pk=pk)

    if request.method == "POST":
        form = ForumForm(request.POST, instance=forum)
        if form.is_valid():
            form.save()
            messages.success(request, "Forum mis à jour.")
            return redirect("forum:liste_forums")
    else:
        form = ForumForm(instance=forum)

    lien_invitation = request.build_absolute_uri(f"/forum/rejoindre/{forum.token_invitation}/")

    return render(request, "forum/modifier_forum.html", {
        "form": form,
        "forum": forum,
        "lien_invitation": lien_invitation,
    })


@user_passes_test(_est_admin)
def basculer_forum(request, pk):
    forum = get_object_or_404(Forum, pk=pk)
    forum.actif = not forum.actif
    forum.save()
    return redirect("forum:liste_forums")


@user_passes_test(_est_admin)
def supprimer_forum(request, pk):
    forum = get_object_or_404(Forum, pk=pk)
    if request.method == "POST":
        forum.delete()
        messages.success(request, "Forum supprimé.")
        return redirect("forum:liste_forums")
    return render(request, "forum/supprimer_forum.html", {"forum": forum})


@user_passes_test(_est_admin)
def gerer_membres(request, pk):
    forum = get_object_or_404(Forum, pk=pk)

    ajout_form = AjoutMembreForm()
    critere_form = AjoutParCritereForm()

    if request.method == "POST":

        if "ajouter_individuel" in request.POST:
            ajout_form = AjoutMembreForm(request.POST)
            if ajout_form.is_valid():
                identifiant = ajout_form.cleaned_data["identifiant"].strip()
                user = CustomUser.objects.filter(username=identifiant).first()
                if not user:
                    user = CustomUser.objects.filter(email=identifiant).first()
                if not user:
                    messages.error(request, "Aucun compte trouvé avec cet identifiant.")
                else:
                    forum.participants.add(user)
                    messages.success(request, f"{user.get_full_name() or user.username} ajouté au forum.")
                return redirect("forum:gerer_membres", pk=forum.pk)

        elif "ajouter_critere" in request.POST:
            critere_form = AjoutParCritereForm(request.POST)
            if critere_form.is_valid():
                role = critere_form.cleaned_data["role"]
                classe = critere_form.cleaned_data["classe"]
                ecole = critere_form.cleaned_data["ecole"]

                nb_ajoutes = 0

                if role == "student":
                    eleves = Eleve.objects.filter(user__isnull=False)
                    if classe:
                        eleves = eleves.filter(classe=classe)
                    elif ecole:
                        eleves = eleves.filter(classe__school=ecole)
                    for eleve in eleves:
                        forum.participants.add(eleve.user)
                        nb_ajoutes += 1

                elif role == "teacher":
                    acces = TeacherSchoolAccess.objects.select_related("teacher__user")
                    if ecole:
                        acces = acces.filter(school=ecole)
                    for a in acces:
                        forum.participants.add(a.teacher.user)
                        nb_ajoutes += 1

                elif role == "staff":
                    staffs = SchoolStaff.objects.select_related("user")
                    if ecole:
                        staffs = staffs.filter(school=ecole)
                    for s in staffs:
                        forum.participants.add(s.user)
                        nb_ajoutes += 1

                elif role in ("parent", "admin"):
                    utilisateurs = CustomUser.objects.filter(role=role)
                    for u in utilisateurs:
                        forum.participants.add(u)
                        nb_ajoutes += 1

                messages.success(request, f"{nb_ajoutes} personne(s) ajoutée(s) au forum.")
                return redirect("forum:gerer_membres", pk=forum.pk)

    lien_invitation = request.build_absolute_uri(f"/forum/rejoindre/{forum.token_invitation}/")

    return render(request, "forum/gerer_membres.html", {
        "forum": forum,
        "ajout_form": ajout_form,
        "critere_form": critere_form,
        "lien_invitation": lien_invitation,
        "membres": forum.participants.all(),
    })


@user_passes_test(_est_admin)
def retirer_membre(request, pk, user_id):
    forum = get_object_or_404(Forum, pk=pk)
    user = get_object_or_404(CustomUser, pk=user_id)
    forum.participants.remove(user)
    messages.success(request, f"{user.get_full_name() or user.username} retiré du forum.")
    return redirect("forum:gerer_membres", pk=forum.pk)