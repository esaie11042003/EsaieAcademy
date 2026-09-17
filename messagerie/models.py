from django.db import models
from django.conf import settings


class Conversation(models.Model):
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="conversations"
    )
    is_support = models.BooleanField(
        default=False,
        verbose_name="Conversation avec l'administration"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def dernier_message(self):
        return self.messages.order_by("-created_at").first()

    def __str__(self):
        noms = ", ".join(
            [u.get_full_name() or u.username for u in self.participants.all()]
        )
        return f"Conversation ({noms})"


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="messages_envoyes"
    )
    body = models.TextField(blank=True)
    fichier = models.FileField(
        upload_to="messagerie/fichiers/",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def est_image(self):
        if not self.fichier:
            return False

        return self.fichier.name.lower().endswith(
            (".jpg", ".jpeg", ".png", ".gif", ".webp")
        )

    def __str__(self):
        return f"{self.sender} — {self.created_at}"


class Lecture(models.Model):
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE
    )
    vu_le = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("utilisateur", "conversation")