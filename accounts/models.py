from django.db import models
from django.contrib.auth.models import AbstractUser


# ============================================================
#
#                MODÈLE : UTILISATEUR
#
# ============================================================
#
# Ce modèle est le modèle utilisateur principal de toute
# la plateforme Esaïe Academy.
#
# Tous les utilisateurs utilisent ce modèle :
#
# • Élèves
# • Enseignants
# • Personnel administratif
# • Administrateur général
#
# Les fonctions précises du personnel
# (Directeur, Censeur, Secrétaire, Comptable...)
# seront gérées dans l'application Configuration.
#
# ============================================================


class CustomUser(AbstractUser):

    # ========================================================
    # RÔLES GÉNÉRAUX
    # ========================================================
    #
    # Ces rôles permettent simplement de savoir
    # dans quelle grande catégorie se trouve
    # l'utilisateur.
    #
    # Les fonctions détaillées du personnel
    # seront gérées par StaffRole.
    #
    # ========================================================

    ROLE_CHOICES = (
        ("student", "Élève"),
        ("teacher", "Enseignant"),
         ("parent", "Parent"),
        ("staff", "Personnel administratif"),
        ("admin", "Administrateur général"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="student",
        verbose_name="Rôle"
    )
    NIVEAU_CHOICES = (
        ("primaire", "Primaire"),
        ("college", "Collège"),
        ("lycee", "Lycée"),
        ("superieur", "Supérieur"),
        ("concours", "Concours professionnel"),
    )

    niveau_etude = models.CharField(
        max_length=20,
        choices=NIVEAU_CHOICES,
        blank=True,
        verbose_name="Niveau d'étude"
    )

    # ========================================================
    # INFORMATIONS PERSONNELLES
    # ========================================================

    SEXE_CHOICES = (
        ("M", "Masculin"),
        ("F", "Féminin"),
    )

    sexe = models.CharField(
        max_length=1,
        choices=SEXE_CHOICES,
        blank=True,
        verbose_name="Sexe"
    )

    date_naissance = models.DateField(
        blank=True,
        null=True,
        verbose_name="Date de naissance"
    )

    adresse = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Adresse"
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Téléphone"
    )

    profile_picture = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
        verbose_name="Photo de profil"
    )

    # ========================================================
    # SÉCURITÉ
    # ========================================================

    # Permet de savoir si le compte
    # a été validé par l'administration.

    is_verified = models.BooleanField(
        default=False,
        verbose_name="Compte vérifié"
    )

    # Obliger l'utilisateur à modifier son mot de passe
    # lors de sa première connexion.

    must_change_password = models.BooleanField(
        default=False,
        verbose_name="Changer le mot de passe"
    )

    # Dernière adresse IP utilisée.

    last_login_ip = models.GenericIPAddressField(
        blank=True,
        null=True,
        verbose_name="Dernière adresse IP"
    )

    # ========================================================
    # ÉTAT DU COMPTE
    # ========================================================

    # Désactive le compte sans supprimer
    # les informations de l'utilisateur.

    actif = models.BooleanField(
        default=True,
        verbose_name="Compte actif"
    )

    # Suppression logique.
    # Les données restent conservées.

    deleted = models.BooleanField(
        default=False,
        verbose_name="Supprimé"
    )

    # ========================================================
    # MÉTADONNÉES
    # ========================================================

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Créé le"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière modification"
    )

    # ========================================================
    # CONFIGURATION DJANGO
    # ========================================================

    class Meta:

        verbose_name = "Utilisateur"

        verbose_name_plural = "Utilisateurs"

        ordering = [
            "last_name",
            "first_name",
        ]

    # ========================================================
    # NOM AFFICHÉ DANS DJANGO
    # ========================================================

    def __str__(self):

        nom = self.get_full_name()

        if nom:

            return nom

        return self.username