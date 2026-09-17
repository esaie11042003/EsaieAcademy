from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, FileResponse
from django.db.models import Q, Case, When, Value, IntegerField

from accounts.models import CustomUser
from .models import Conversation, Message, Lecture
from .forms import MessageForm, RechercheUtilisateurForm


def _label_conversation(conversation, viewer):
    if conversation.is_support:
        if viewer.role == "admin":
            autres = conversation.participants.exclude(role="admin")
            if not autres.exists():
                autres = conversation.participants.exclude(pk=viewer.pk)
            noms = ", ".join([u.get_full_name() or u.username for u in autres])
            return noms or "Demande d'assistance"
        else:
            return "Administration Esaïe Academy"
    else:
        autres = conversation.participants.exclude(pk=viewer.pk)
        return ", ".join([u.get_full_name() or u.username for u in autres])


@login_required
def inbox(request):

    if request.user.role == "admin":
        conversations = (
            Conversation.objects.filter(participants=request.user) |
            Conversation.objects.filter(is_support=True)
        ).distinct()
    else:
        conversations = Conversation.objects.filter(participants=request.user)

    liste = []
    for c in conversations:
        liste.append({
            "conversation": c,
            "label": _label_conversation(c, request.user),
            "dernier": c.dernier_message(),
        })

    liste.sort(key=lambda x: x["dernier"].created_at if x["dernier"] else x["conversation"].created_at, reverse=True)

    return render(request, "messagerie/inbox.html", {"liste": liste})


@login_required
def nouvelle_conversation(request):

    if request.method == "POST":
        form = RechercheUtilisateurForm(request.POST)
        if form.is_valid():
            identifiant = form.cleaned_data["identifiant"]

            destinataire = CustomUser.objects.filter(username=identifiant).first()
            if not destinataire:
                destinataire = CustomUser.objects.filter(email=identifiant).first()

            if not destinataire:
                messages.error(request, "Aucun compte trouvé avec cet identifiant.")
            elif destinataire == request.user:
                messages.error(request, "Vous ne pouvez pas discuter avec vous-même.")
            else:
                conversation = Conversation.objects.filter(
                    is_support=False, participants=request.user
                ).filter(participants=destinataire).first()

                if not conversation:
                    conversation = Conversation.objects.create()
                    conversation.participants.add(request.user, destinataire)

                return redirect("messagerie:conversation_detail", pk=conversation.pk)
    else:
        form = RechercheUtilisateurForm()

    return render(request, "messagerie/nouvelle_conversation.html", {"form": form})


@login_required
def contacter_admins(request):

    conversation = Conversation.objects.filter(is_support=True, participants=request.user).first()

    if not conversation:
        conversation = Conversation.objects.create(is_support=True)
        conversation.participants.add(request.user)
        admins = CustomUser.objects.filter(role="admin")
        conversation.participants.add(*admins)

    return redirect("messagerie:conversation_detail", pk=conversation.pk)


@login_required
def conversation_detail(request, pk):

    conversation = get_object_or_404(Conversation, pk=pk)

    autorise = conversation.participants.filter(pk=request.user.pk).exists() or (
        conversation.is_support and request.user.role == "admin"
    )

    if not autorise:
        messages.error(request, "Vous n'avez pas accès à cette conversation.")
        return redirect("messagerie:inbox")

    if request.user.role == "admin" and conversation.is_support:
        conversation.participants.add(request.user)

    if request.method == "POST":
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data["body"] or form.cleaned_data["fichier"]:
                msg = form.save(commit=False)
                msg.conversation = conversation
                msg.sender = request.user
                msg.save()
            return redirect("messagerie:conversation_detail", pk=pk)
    else:
        form = MessageForm()

    Lecture.objects.update_or_create(utilisateur=request.user, conversation=conversation)

    liste_messages = conversation.messages.select_related("sender")
    label = _label_conversation(conversation, request.user)

    return render(request, "messagerie/conversation_detail.html", {
        "conversation": conversation,
        "messages_liste": liste_messages,
        "label": label,
        "form": form,
    })


@login_required
def rechercher_utilisateurs(request):
    """
    Recherche insensible à la casse : les noms/prénoms qui COMMENCENT
    par le terme tapé apparaissent en premier (triés par ordre alphabétique),
    suivis de tous ceux qui contiennent simplement le terme quelque part.
    """
    terme = request.GET.get("q", "").strip()

    if len(terme) < 1:
        return JsonResponse({"resultats": []})

    utilisateurs = CustomUser.objects.filter(
        Q(username__icontains=terme) |
        Q(first_name__icontains=terme) |
        Q(last_name__icontains=terme)
    ).exclude(pk=request.user.pk).annotate(
        priorite=Case(
            When(first_name__istartswith=terme, then=Value(0)),
            When(last_name__istartswith=terme, then=Value(0)),
            When(username__istartswith=terme, then=Value(1)),
            default=Value(2),
            output_field=IntegerField(),
        )
    ).order_by("priorite", "first_name", "last_name")[:15]

    resultats = [
        {
            "username": u.username,
            "nom": u.get_full_name() or u.username,
            "role": u.get_role_display(),
        }
        for u in utilisateurs
    ]

    return JsonResponse({"resultats": resultats})


@login_required
def telecharger_fichier(request, pk):
    message = get_object_or_404(Message, pk=pk)
    conversation = message.conversation

    autorise = conversation.participants.filter(pk=request.user.pk).exists() or (
        conversation.is_support and request.user.role == "admin"
    )
    if not autorise or not message.fichier:
        messages.error(request, "Fichier introuvable.")
        return redirect("messagerie:inbox")

    return FileResponse(message.fichier.open("rb"), as_attachment=True, filename=message.fichier.name.split("/")[-1])