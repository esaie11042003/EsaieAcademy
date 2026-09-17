import uuid

from django.db import models
from django.conf import settings


class Forum(models.Model):

    nom = models.CharField(max_length=150, verbose_name="Nom du forum")
    description = models.TextField(blank=True, verbose_name="Description")
    actif = models.BooleanField(default=True, verbose_name="Actif")

    cree_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="forums_crees",
        verbose_name="Créé par"
    )

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="forums",
        blank=True,
        verbose_name="Participants"
    )

    token_invitation = models.CharField(
        max_length=32, unique=True, blank=True,
        verbose_name="Jeton d'invitation"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Forum"
        verbose_name_plural = "Forums"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.token_invitation:
            self.token_invitation = uuid.uuid4().hex[:12]
        super().save(*args, **kwargs)

    def dernier_message(self):
        return self.messages.order_by("-created_at").first()

    def __str__(self):
        return self.nom


class ForumMessage(models.Model):

    forum = models.ForeignKey(
        Forum,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="messages_forum"
    )
    contenu = models.TextField(blank=True)
    fichier = models.FileField(
        upload_to="forum/fichiers/",
        blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Message du forum"
        verbose_name_plural = "Messages du forum"

    def est_image(self):
        if not self.fichier:
            return False
        return self.fichier.name.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp"))

    def __str__(self):
        return f"{self.auteur} — {self.forum}"