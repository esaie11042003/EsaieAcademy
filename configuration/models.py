from django.db import models
from django.utils.text import slugify

from accounts.models import CustomUser


# ============================================================
#
#                MODÈLE : ÉTABLISSEMENT
#
# ============================================================
#
# Ce modèle représente un établissement scolaire.
#
# Toute la plateforme repose sur ce modèle.
#
# Exemples :
#
# - Collège Catholique Saint Michel
# - CEG Akpakpa
# - CPEG Sainte Rita
#
# Toutes les autres applications utiliseront ces
# informations.
#
# ============================================================

class SchoolProfile(models.Model):

    # ========================================================
    # TYPE D'ÉTABLISSEMENT
    # ========================================================
    #
    # Public ou Privé.
    #
    # Le choix est volontairement limité car ces valeurs
    # ne changent presque jamais.
    #
    # ========================================================

    TYPE_ETABLISSEMENT = (
        ("public", "Public"),
        ("prive", "Privé"),
    )

    # ========================================================
    # IDENTIFICATION
    # ========================================================

    # Code unique de l'établissement.
    #
    # Exemples :
    #
    # ESA001
    # CEG001
    # CSP001

    code_etablissement = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Code établissement"
    )

    # Nom officiel.

    nom = models.CharField(
        max_length=200,
        verbose_name="Nom"
    )

    # Sigle.
    #
    # Exemple :
    #
    # CEG
    # CSMJ
    # CSP

    sigle = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Sigle"
    )

    # Utilisé dans les URLs.

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    # Public ou Privé.

    type_etablissement = models.CharField(
        max_length=20,
        choices=TYPE_ETABLISSEMENT,
        default="prive",
        verbose_name="Type"
    )

    # Devise officielle.

    devise = models.CharField(
        max_length=255,
        blank=True
    )

    # ========================================================
    # IMAGES
    # ========================================================

    # Logo officiel.

    logo = models.ImageField(
        upload_to="configuration/logo/",
        blank=True,
        null=True
    )

    cachet = models.ImageField(
        upload_to="configuration/cachets/",
        blank=True,
        null=True,
        verbose_name="Cachet / Tampon de l'établissement"
    )

    # Grande image de présentation.

    photo_couverture = models.ImageField(
        upload_to="configuration/couverture/",
        blank=True,
        null=True
    )

    # ========================================================
    # DESCRIPTION
    # ========================================================

    description = models.TextField(
        blank=True
    )

    # ========================================================
    # LOCALISATION
    # ========================================================

    adresse = models.CharField(
        max_length=255,
        blank=True
    )

    quartier = models.CharField(
        max_length=100,
        blank=True
    )

    ville = models.CharField(
        max_length=100,
        blank=True
    )

    departement = models.CharField(
        max_length=100,
        blank=True
    )

    pays = models.CharField(
        max_length=100,
        default="Bénin"
    )

    # ========================================================
    # CONTACTS
    # ========================================================

    telephone = models.CharField(
        max_length=30,
        blank=True
    )

    telephone_secondaire = models.CharField(
        max_length=30,
        blank=True
    )

    whatsapp = models.CharField(
        max_length=30,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    site_web = models.URLField(
        blank=True
    )

    # ========================================================
    # FUTUR SOUS-DOMAINE
    # ========================================================
    #
    # Exemple :
    #
    # saint-michel
    #
    # deviendra
    #
    # saint-michel.esaieacademy.com
    #
    # ========================================================

    subdomain = models.CharField(
        max_length=100,
        blank=True
    )

    # Fuseau horaire.

    timezone = models.CharField(
        max_length=100,
        default="Africa/Porto-Novo"
    )

    # ========================================================
    # INFORMATIONS ADMINISTRATIVES
    # ========================================================

    date_creation = models.DateField(
        blank=True,
        null=True
    )

    numero_autorisation = models.CharField(
        max_length=100,
        blank=True
    )

    ifu = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="IFU / NIF"
    )

    # ========================================================
    # PARAMÈTRES
    # ========================================================

    actif = models.BooleanField(
        default=True
    )

    # ========================================================
    # MÉTADONNÉES
    # ========================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # ========================================================
    # CONFIGURATION DJANGO
    # ========================================================

    class Meta:

        verbose_name = "Établissement"

        verbose_name_plural = "Établissements"

        ordering = ["nom"]

    # ========================================================
    # GÉNÉRATION AUTOMATIQUE DU SLUG
    # ========================================================

    def save(self, *args, **kwargs):

        if not self.slug:

            self.slug = slugify(self.nom)

        super().save(*args, **kwargs)

    # ========================================================
    # REPRÉSENTATION TEXTUELLE
    # ========================================================

    def __str__(self):

        return self.nom
    # ============================================================
#
#                MODÈLE : FONCTIONS
#
# ============================================================
#
# Ce modèle contient toutes les fonctions administratives
# d'un établissement.
#
# Exemples :
#
# - Directeur
# - Directeur adjoint
# - Censeur
# - Censeur adjoint
# - Secrétaire
# - Comptable
# - Responsable informatique
# - Bibliothécaire
#
# L'avantage de ce modèle est que le directeur pourra
# créer autant de nouvelles fonctions qu'il le souhaite
# sans modifier le code.
#
# ============================================================

class StaffRole(models.Model):

    # --------------------------------------------------------
    # Établissement concerné
    # --------------------------------------------------------

    school = models.ForeignKey(
        SchoolProfile,
        on_delete=models.CASCADE,
        related_name="roles",
        verbose_name="Établissement"
    )

    # --------------------------------------------------------
    # Nom de la fonction
    # --------------------------------------------------------

    nom = models.CharField(
        max_length=100,
        verbose_name="Fonction"
    )

    # --------------------------------------------------------
    # Description facultative
    # --------------------------------------------------------

    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )

    # --------------------------------------------------------
    # Ordre d'affichage
    #
    # Exemple :
    #
    # 1 Directeur
    # 2 Directeur adjoint
    # 3 Censeur
    # 4 Secrétaire
    #
    # --------------------------------------------------------

    ordre = models.PositiveIntegerField(
        default=1,
        verbose_name="Ordre"
    )

    # --------------------------------------------------------
    # Fonction active ou non
    # --------------------------------------------------------

    actif = models.BooleanField(
        default=True
    )

    # --------------------------------------------------------
    # Dates de création
    # --------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        verbose_name = "Fonction"

        verbose_name_plural = "Fonctions"

        ordering = [
            "ordre",
            "nom"
        ]

        unique_together = (
            "school",
            "nom"
        )

    def __str__(self):

        return self.nom


# ============================================================
#
#                MODÈLE : RESPONSABLES
#
# ============================================================
#
# Ce modèle représente les différents responsables
# d'un établissement.
#
# Toutes ces informations existent déjà
# dans CustomUser.
#
# Ce modèle contient uniquement les informations
# propres au poste occupé.
#
# ============================================================

class SchoolStaff(models.Model):

    # --------------------------------------------------------
    # Établissement
    # --------------------------------------------------------

    school = models.ForeignKey(
        SchoolProfile,
        on_delete=models.CASCADE,
        related_name="staff_members",
        verbose_name="Établissement"
    )

    # --------------------------------------------------------
    # Utilisateur
    #
    # Toutes les informations personnelles
    # proviennent du compte utilisateur.
    # --------------------------------------------------------

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="school_staff",
        verbose_name="Utilisateur"
    )

    # --------------------------------------------------------
    # Fonction occupée
    # --------------------------------------------------------

    role = models.ForeignKey(
        StaffRole,
        on_delete=models.PROTECT,
        related_name="staff",
        verbose_name="Fonction"
    )

    # --------------------------------------------------------
    # Signature officielle
    #
    # Utilisée pour :
    #
    # - Bulletins
    # - Attestations
    # - Relevés
    # - Diplômes
    #
    # --------------------------------------------------------

    signature = models.ImageField(
        upload_to="configuration/staff/signatures/",
        blank=True,
        null=True,
        verbose_name="Signature"
    )

    # --------------------------------------------------------
    # Ordre d'affichage des signatures
    #
    # Exemple :
    #
    # 1 Directeur
    # 2 Censeur
    # 3 Secrétaire
    #
    # --------------------------------------------------------

    ordre_signature = models.PositiveIntegerField(
        default=1,
        verbose_name="Ordre de signature"
    )

    # --------------------------------------------------------
    # Afficher la signature sur les documents ?
    # --------------------------------------------------------

    afficher_signature = models.BooleanField(
        default=True,
        verbose_name="Afficher la signature"
    )

    # --------------------------------------------------------
    # Responsable actif ?
    # --------------------------------------------------------

    actif = models.BooleanField(
        default=True
    )

    # --------------------------------------------------------
    # Dates
    # --------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        verbose_name = "Responsable"

        verbose_name_plural = "Responsables"

        ordering = [
            "ordre_signature",
            "role"
        ]

    # --------------------------------------------------------
    # Nom affiché dans Django
    # --------------------------------------------------------

    def __str__(self):

        nom = self.user.get_full_name()

        if not nom:
            nom = self.user.username

        return f"{nom} - {self.role}"

# Ajout : statut de validation par l'administration générale
SchoolProfile.add_to_class(
    "statut_validation",
    models.CharField(
        max_length=20,
        choices=(
            ("en_attente", "En attente de validation"),
            ("valide", "Validé"),
            ("rejete", "Rejeté"),
        ),
        default="en_attente",
        verbose_name="Statut de validation",
    ),
)
