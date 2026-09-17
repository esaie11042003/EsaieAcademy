from .models import Conversation, Lecture


def messages_widget(request):
    if not request.user.is_authenticated:
        return {}

    if request.user.role == "admin":
        conversations = (Conversation.objects.filter(participants=request.user) | Conversation.objects.filter(is_support=True)).distinct()
    else:
        conversations = Conversation.objects.filter(participants=request.user)

    items = []
    non_lus = 0

    for c in conversations:
        dernier = c.dernier_message()
        if not dernier:
            continue
        lecture = Lecture.objects.filter(utilisateur=request.user, conversation=c).first()
        est_non_lu = dernier.sender != request.user and (not lecture or dernier.created_at > lecture.vu_le)
        if est_non_lu:
            non_lus += 1
        items.append({"conversation": c, "dernier": dernier, "non_lu": est_non_lu})

    items.sort(key=lambda x: x["dernier"].created_at, reverse=True)

    return {
        "msg_recents": items[:5],
        "msg_non_lus_total": non_lus,
    }