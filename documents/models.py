"""
==========================================================
                MODELS - DOCUMENTS
==========================================================

Application : Documents
Projet : Esaïe Academy

Cette application gère toute la bibliothèque numérique.

Elle permet de gérer :

• Les cours
• Les exercices
• Les travaux dirigés (TD)
• Les travaux pratiques (TP)
• Les devoirs
• Les interrogations
• Les évaluations
• Les examens
• Les concours
• Les corrigés
• Les livres
• Les PDF
• Les vidéos
• Les images
• Les fichiers audio

Compatible avec :

✔ Accounts
✔ Students
✔ Teachers
✔ Subjects
✔ Classes
✔ School
✔ Payments

==========================================================
"""

import uuid

from django.db import models
from django.utils import timezone


# ==========================================================
#                  CLASSE DE BASE
# ==========================================================

class BaseDocumentModel(models.Model):
    """
    Classe abstraite utilisée par tous les modèles
    de l'application Documents.
    """

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="Identifiant unique"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Créé le"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Modifié le"
    )

    active = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )

    class Meta:
        abstract = True
        # ==========================================================
#              CATÉGORIES DES DOCUMENTS
# ==========================================================

class DocumentCategory(BaseDocumentModel):
    """
    Catégories principales des ressources pédagogiques.

    Exemples :

    - Cours
    - Exercices
    - Travaux dirigés
    - Travaux pratiques
    - Devoirs
    - Interrogations
    - Évaluations
    - Examens
    - Concours
    - Corrigés
    - Livres
    - Documents administratifs
    """

    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Nom de la catégorie"
    )

    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Code"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Icône"
    )

    color = models.CharField(
        max_length=20,
        default="#1976D2",
        verbose_name="Couleur"
    )

    display_order = models.PositiveIntegerField(
        default=1,
        verbose_name="Ordre d'affichage"
    )

    class Meta:
        verbose_name = "Catégorie de document"
        verbose_name_plural = "Catégories de documents"
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name
    # ==========================================================
#                 TYPES DE DOCUMENTS
# ==========================================================

class DocumentType(BaseDocumentModel):
    """
    Types de fichiers pouvant être publiés.

    Exemples :

    - PDF
    - Word
    - Excel
    - PowerPoint
    - Image
    - Audio
    - Vidéo
    - Archive ZIP
    """

    FILE_TYPE_CHOICES = [
        ("pdf", "PDF"),
        ("word", "Microsoft Word"),
        ("excel", "Microsoft Excel"),
        ("powerpoint", "Microsoft PowerPoint"),
        ("image", "Image"),
        ("audio", "Audio"),
        ("video", "Vidéo"),
        ("zip", "Archive ZIP"),
        ("other", "Autre"),
    ]

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nom"
    )

    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Code"
    )

    file_type = models.CharField(
        max_length=30,
        choices=FILE_TYPE_CHOICES,
        verbose_name="Type de fichier"
    )

    extension = models.CharField(
        max_length=20,
        verbose_name="Extension"
    )

    mime_type = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Type MIME"
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Icône"
    )

    color = models.CharField(
        max_length=20,
        default="#4CAF50",
        verbose_name="Couleur"
    )

    max_size_mb = models.PositiveIntegerField(
        default=100,
        verbose_name="Taille maximale (Mo)"
    )

    display_order = models.PositiveIntegerField(
        default=1,
        verbose_name="Ordre d'affichage"
    )

    class Meta:
        verbose_name = "Type de document"
        verbose_name_plural = "Types de documents"
        ordering = ["display_order", "name"]

    def __str__(self):
        return f"{self.name} (*.{self.extension})"
        # ==========================================================
#                    DOCUMENTS
# ==========================================================

class DocumentSeries(BaseDocumentModel):
    """
    Séries concernées par un document (ex : Série A, C, D, F, G...).

    Permet de cibler un document pour une ou plusieurs
    séries de la filière secondaire/université.
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nom de la série"
    )

    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Code"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )

    display_order = models.PositiveIntegerField(
        default=1,
        verbose_name="Ordre d'affichage"
    )

    class Meta:
        verbose_name = "Série"
        verbose_name_plural = "Séries"
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name
    # ==========================================================
#                    DOCUMENTS
# ==========================================================

class Document(BaseDocumentModel):
    """
    Modèle principal représentant une ressource pédagogique.

    Un document peut être :

    • un cours
    • un exercice
    • un TD
    • un TP
    • un devoir
    • une interrogation
    • une évaluation
    • un examen
    • un concours
    • un corrigé
    • un livre
    • etc.
    """

    ACCESS_CHOICES = [
        ("free", "Gratuit"),
        ("premium", "Réservé Premium"),
        ("paid", "Payant"),
        ("school", "Réservé aux établissements"),
    ]

    LEVEL_CHOICES = [
        ("primary", "Primaire"),
        ("secondary", "Secondaire"),
        ("university", "Université"),
        ("other", "Autre"),
    ]

    title = models.CharField(
        max_length=255,
        verbose_name="Titre"
    )

    slug = models.SlugField(
        unique=True,
        verbose_name="Slug"
    )

    category = models.ForeignKey(
        "DocumentCategory",
        on_delete=models.PROTECT,
        related_name="documents",
        verbose_name="Catégorie"
    )

    document_type = models.ForeignKey(
        "DocumentType",
        on_delete=models.PROTECT,
        related_name="documents",
        verbose_name="Type de document"
    )

    subject = models.ForeignKey(
        "subjects.Subject",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="documents",
        verbose_name="Matière"
    )

    classe = models.ForeignKey(
        "classes.Classe",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="documents",
        verbose_name="Classe"
    )

    school_year = models.ForeignKey(
        "school.SchoolYear",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="documents",
        verbose_name="Année scolaire"
    )

    teacher = models.ForeignKey(
        "teachers.Teacher",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="documents",
        verbose_name="Auteur"
    )

    level = models.CharField(
        max_length=30,
        choices=LEVEL_CHOICES,
        default="secondary",
        verbose_name="Niveau"
    )

    access_type = models.CharField(
        max_length=20,
        choices=ACCESS_CHOICES,
        default="free",
        verbose_name="Accès"
    )
    prix = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        null=True,
        blank=True,
        verbose_name="Prix (FCFA)"
    )

    short_description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Description courte"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Description complète"
    )

    cover_image = models.ImageField(
        upload_to="documents/covers/",
        blank=True,
        null=True,
        verbose_name="Image de couverture"
    )

    featured = models.BooleanField(
        default=False,
        verbose_name="Document à la une"
    )

    downloadable = models.BooleanField(
        default=True,
        verbose_name="Téléchargeable"
    )
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    published = models.BooleanField(
        default=True,
        verbose_name="Publié"
    )

    publication_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="Date de publication"
    )

    series = models.ManyToManyField(
        "DocumentSeries",
        blank=True,
        related_name="documents",
        verbose_name="Séries concernées"
    )

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"
        ordering = ["-publication_date", "title"]

    def __str__(self):
        return self.title
    # ==========================================================
#                 FICHIERS DES DOCUMENTS
# ==========================================================

class DocumentFile(BaseDocumentModel):
    """
    Représente un fichier associé à un document.

    Un même document peut contenir plusieurs fichiers :
    - PDF
    - Word
    - Excel
    - PowerPoint
    - Vidéo
    - Audio
    - Image
    - Archive ZIP
    """

    document = models.ForeignKey(
        "Document",
        on_delete=models.CASCADE,
        related_name="files",
        verbose_name="Document"
    )

    file_type = models.ForeignKey(
        "DocumentType",
        on_delete=models.PROTECT,
        related_name="files",
        verbose_name="Type de fichier"
    )

    title = models.CharField(
        max_length=255,
        verbose_name="Titre du fichier"
    )

    file = models.FileField(
        upload_to="documents/files/",
        verbose_name="Fichier"
    )

    version = models.CharField(
        max_length=20,
        default="1.0",
        verbose_name="Version"
    )

    file_size = models.PositiveBigIntegerField(
        default=0,
        verbose_name="Taille (octets)"
    )

    download_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Nombre de téléchargements"
    )

    is_main_file = models.BooleanField(
        default=True,
        verbose_name="Fichier principal"
    )

    class Meta:
        verbose_name = "Fichier du document"
        verbose_name_plural = "Fichiers des documents"
        ordering = ["document", "title"]

    def __str__(self):
        return f"{self.document.title} - {self.title}"
    # ==========================================================
#                    TAGS DES DOCUMENTS
# ==========================================================

class DocumentTag(BaseDocumentModel):
    """
    Mots-clés associés aux documents.

    Ils facilitent :

    • la recherche
    • le filtrage
    • les recommandations
    • les statistiques
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nom du tag"
    )

    slug = models.SlugField(
        unique=True,
        verbose_name="Slug"
    )

    color = models.CharField(
        max_length=20,
        default="#2196F3",
        verbose_name="Couleur"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["name"]

    def __str__(self):
        return self.name


# ==========================================================
#              ASSOCIATION DOCUMENT <-> TAG
# ==========================================================

class DocumentTagRelation(BaseDocumentModel):
    """
    Association entre un document
    et un ou plusieurs tags.
    """

    document = models.ForeignKey(
        "Document",
        on_delete=models.CASCADE,
        related_name="tag_relations",
        verbose_name="Document"
    )

    tag = models.ForeignKey(
        "DocumentTag",
        on_delete=models.CASCADE,
        related_name="document_relations",
        verbose_name="Tag"
    )

    class Meta:
        verbose_name = "Association document/tag"
        verbose_name_plural = "Associations documents/tags"
        unique_together = ("document", "tag")
        ordering = ["document"]

    def __str__(self):
        return f"{self.document.title} → {self.tag.name}"
    # ==========================================================
#          HISTORIQUE DES TÉLÉCHARGEMENTS
# ==========================================================

class DocumentDownload(BaseDocumentModel):
    """
    Historique des téléchargements.

    Chaque téléchargement est enregistré afin de :

    • connaître le nombre réel de téléchargements
    • contrôler les accès
    • établir des statistiques
    • lutter contre la fraude
    """

    DOWNLOAD_STATUS = [
        ("authorized", "Autorisé"),
        ("blocked", "Bloqué"),
        ("expired", "Lien expiré"),
    ]

    document = models.ForeignKey(
        "Document",
        on_delete=models.CASCADE,
        related_name="downloads",
        verbose_name="Document"
    )

    user = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="document_downloads",
        verbose_name="Utilisateur"
    )

    file = models.ForeignKey(
        "DocumentFile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="downloads",
        verbose_name="Fichier"
    )

    download_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de téléchargement"
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="Adresse IP"
    )

    device = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Appareil"
    )

    browser = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Navigateur"
    )

    operating_system = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Système d'exploitation"
    )

    status = models.CharField(
        max_length=20,
        choices=DOWNLOAD_STATUS,
        default="authorized",
        verbose_name="Statut"
    )

    payment_verified = models.BooleanField(
        default=False,
        verbose_name="Paiement vérifié"
    )

    class Meta:
        verbose_name = "Téléchargement"
        verbose_name_plural = "Téléchargements"
        ordering = ["-download_date"]

    def __str__(self):
        utilisateur = self.user.username if self.user else "Utilisateur inconnu"
        return f"{utilisateur} → {self.document.title}"
    # ==========================================================
#                DOCUMENTS FAVORIS
# ==========================================================

class DocumentFavorite(BaseDocumentModel):
    """
    Permet à un utilisateur d'ajouter
    un document à sa liste de favoris.

    Cette fonctionnalité facilite
    l'accès rapide aux ressources
    les plus utilisées.
    """

    user = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.CASCADE,
        related_name="favorite_documents",
        verbose_name="Utilisateur"
    )

    document = models.ForeignKey(
        "Document",
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Document"
    )

    favorite_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'ajout"
    )

    note = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Note personnelle"
    )

    class Meta:
        verbose_name = "Document favori"
        verbose_name_plural = "Documents favoris"
        ordering = ["-favorite_date"]
        unique_together = ("user", "document")

    def __str__(self):
        return f"{self.user} ❤️ {self.document.title}"
    # ==========================================================
#              COMMENTAIRES DES DOCUMENTS
# ==========================================================

class DocumentComment(BaseDocumentModel):
    """
    Commentaires publiés sous un document.

    Les commentaires permettent :

    • aux élèves de poser des questions
    • aux enseignants d'apporter des réponses
    • aux administrateurs de modérer les échanges
    """

    document = models.ForeignKey(
        "Document",
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Document"
    )

    user = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.CASCADE,
        related_name="document_comments",
        verbose_name="Auteur"
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
        verbose_name="Commentaire parent"
    )

    comment = models.TextField(
        verbose_name="Commentaire"
    )

    rating = models.PositiveSmallIntegerField(
        default=5,
        verbose_name="Note (sur 5)"
    )

    likes = models.PositiveIntegerField(
        default=0,
        verbose_name="Likes"
    )

    dislikes = models.PositiveIntegerField(
        default=0,
        verbose_name="Dislikes"
    )

    is_approved = models.BooleanField(
        default=True,
        verbose_name="Approuvé"
    )

    is_pinned = models.BooleanField(
        default=False,
        verbose_name="Épinglé"
    )

    is_reported = models.BooleanField(
        default=False,
        verbose_name="Signalé"
    )

    report_reason = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Motif du signalement"
    )

    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.document.title}"
    # ==========================================================
#            ACCÈS AUX DOCUMENTS
# ==========================================================

class DocumentAccess(BaseDocumentModel):
    """
    Gestion des autorisations d'accès
    aux documents.

    Ce modèle permettra de vérifier
    si un utilisateur peut consulter
    ou télécharger un document.
    """

    ACCESS_STATUS = [
        ("active", "Actif"),
        ("expired", "Expiré"),
        ("blocked", "Bloqué"),
    ]

    user = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.CASCADE,
        related_name="document_access",
        verbose_name="Utilisateur"
    )

    document = models.ForeignKey(
        "Document",
        on_delete=models.CASCADE,
        related_name="authorized_users",
        verbose_name="Document"
    )

    status = models.CharField(
        max_length=20,
        choices=ACCESS_STATUS,
        default="active",
        verbose_name="Statut"
    )

    start_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="Début d'accès"
    )

    end_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fin d'accès"
    )

    unlimited = models.BooleanField(
        default=True,
        verbose_name="Accès illimité"
    )

    class Meta:
        verbose_name = "Accès au document"
        verbose_name_plural = "Accès aux documents"
        ordering = ["-created_at"]
        unique_together = ("user", "document")

    def __str__(self):
        return f"{self.user} → {self.document.title}"
    # ==========================================================
#              HISTORIQUE DES CONSULTATIONS
# ==========================================================

class DocumentView(BaseDocumentModel):
    """
    Historique des consultations des documents.

    Ce modèle permet de connaître :

    • qui a consulté un document ;
    • combien de fois il a été consulté ;
    • depuis quelle adresse IP ;
    • depuis quel appareil.

    Ces informations serviront aux statistiques
    et à la sécurité.
    """

    document = models.ForeignKey(
        "Document",
        on_delete=models.CASCADE,
        related_name="views",
        verbose_name="Document"
    )

    user = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="document_views",
        verbose_name="Utilisateur"
    )

    viewed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de consultation"
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="Adresse IP"
    )

    device = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Appareil"
    )

    browser = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Navigateur"
    )

    operating_system = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Système d'exploitation"
    )

    class Meta:
        verbose_name = "Consultation"
        verbose_name_plural = "Consultations"
        ordering = ["-viewed_at"]

    def __str__(self):
        utilisateur = self.user.username if self.user else "Visiteur"

        return f"{utilisateur} → {self.document.title}"
    # ==========================================================
#              NOTES DES DOCUMENTS
# ==========================================================

class DocumentRating(BaseDocumentModel):
    """
    Permet aux utilisateurs d'attribuer
    une note à un document.

    Ces notes serviront à :

    • calculer la moyenne des évaluations ;
    • classer les meilleurs documents ;
    • afficher les étoiles sur la plateforme.
    """

    document = models.ForeignKey(
        "Document",
        on_delete=models.CASCADE,
        related_name="ratings",
        verbose_name="Document"
    )

    user = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.CASCADE,
        related_name="document_ratings",
        verbose_name="Utilisateur"
    )

    rating = models.PositiveSmallIntegerField(
        default=5,
        verbose_name="Nombre d'étoiles"
    )

    review = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Avis rapide"
    )

    class Meta:
        verbose_name = "Note du document"
        verbose_name_plural = "Notes des documents"
        ordering = ["-created_at"]
        unique_together = ("document", "user")

    def __str__(self):
        return f"{self.document.title} - {self.rating}/5"
    # ==========================================================
#               SIGNETS DES DOCUMENTS
# ==========================================================

class DocumentBookmark(BaseDocumentModel):
    """
    Permet à un utilisateur d'enregistrer
    sa position dans un document.

    Cette fonctionnalité permet de reprendre
    la lecture exactement au bon endroit.
    """

    user = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.CASCADE,
        related_name="document_bookmarks",
        verbose_name="Utilisateur"
    )

    document = models.ForeignKey(
        "Document",
        on_delete=models.CASCADE,
        related_name="bookmarks",
        verbose_name="Document"
    )

    page_number = models.PositiveIntegerField(
        default=1,
        verbose_name="Numéro de page"
    )

    video_position = models.PositiveIntegerField(
        default=0,
        verbose_name="Position vidéo (secondes)"
    )

    note = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Note personnelle"
    )

    class Meta:
        verbose_name = "Signet"
        verbose_name_plural = "Signets"
        ordering = ["-updated_at"]
        unique_together = ("user", "document")

    def __str__(self):
        return f"{self.user} - {self.document.title}"
    # ==========================================================
#             PARTAGE DES DOCUMENTS
# ==========================================================

class DocumentShare(BaseDocumentModel):
    """
    Gestion du partage des documents.

    Permet de savoir :

    • qui partage ;
    • avec qui ;
    • quel document ;
    • pendant combien de temps.

    Les documents payants pourront être protégés
    contre le partage non autorisé.
    """

    SHARE_TYPES = [
        ("private", "Privé"),
        ("student", "Élève"),
        ("teacher", "Enseignant"),
        ("class", "Classe"),
        ("school", "Établissement"),
        ("public", "Public"),
    ]

    document = models.ForeignKey(
        "Document",
        on_delete=models.CASCADE,
        related_name="shares",
        verbose_name="Document"
    )

    shared_by = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.CASCADE,
        related_name="shared_documents",
        verbose_name="Partagé par"
    )

    shared_with = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="received_documents",
        verbose_name="Partagé avec"
    )

    share_type = models.CharField(
        max_length=20,
        choices=SHARE_TYPES,
        default="private",
        verbose_name="Type de partage"
    )

    access_start = models.DateTimeField(
        default=timezone.now,
        verbose_name="Début d'accès"
    )

    access_end = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fin d'accès"
    )

    download_allowed = models.BooleanField(
        default=True,
        verbose_name="Téléchargement autorisé"
    )

    active = models.BooleanField(
        default=True,
        verbose_name="Partage actif"
    )

    class Meta:
        verbose_name = "Partage de document"
        verbose_name_plural = "Partages des documents"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.document.title} ({self.shared_by})"
    # ==========================================================
#            JOURNAL DE SÉCURITÉ DES DOCUMENTS
# ==========================================================

class DocumentSecurityLog(BaseDocumentModel):
    """
    Historique des actions de sécurité
    effectuées sur les documents.

    Ce modèle permet de tracer toutes les
    opérations sensibles afin d'améliorer
    la sécurité de la plateforme.
    """

    ACTION_CHOICES = [
        ("view", "Consultation"),
        ("download", "Téléchargement"),
        ("upload", "Ajout"),
        ("update", "Modification"),
        ("delete", "Suppression"),
        ("share", "Partage"),
        ("blocked", "Accès refusé"),
        ("login", "Connexion"),
        ("other", "Autre"),
    ]

    document = models.ForeignKey(
        "Document",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="security_logs",
        verbose_name="Document"
    )

    user = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="document_security_logs",
        verbose_name="Utilisateur"
    )

    action = models.CharField(
        max_length=30,
        choices=ACTION_CHOICES,
        verbose_name="Action"
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="Adresse IP"
    )

    device = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Appareil"
    )

    browser = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Navigateur"
    )

    operating_system = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Système d'exploitation"
    )

    success = models.BooleanField(
        default=True,
        verbose_name="Opération réussie"
    )

    message = models.TextField(
        blank=True,
        verbose_name="Message"
    )

    class Meta:
        verbose_name = "Journal de sécurité"
        verbose_name_plural = "Journaux de sécurité"
        ordering = ["-created_at"]

    def __str__(self):
        utilisateur = self.user.username if self.user else "Inconnu"
        return f"{utilisateur} - {self.action}"
    # ==========================================================
#              COLLECTIONS DE DOCUMENTS
# ==========================================================

class DocumentCollection(BaseDocumentModel):
    """
    Permet de regrouper plusieurs documents
    dans une même collection.

    Exemples :

    • Mathématiques 3ème
    • BAC Série C
    • CEP 2026
    • Concours ENS
    """

    title = models.CharField(
        max_length=255,
        verbose_name="Titre"
    )

    slug = models.SlugField(
        unique=True,
        verbose_name="Slug"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )

    image = models.ImageField(
        upload_to="documents/collections/",
        blank=True,
        null=True,
        verbose_name="Image"
    )

    documents = models.ManyToManyField(
        "Document",
        related_name="collections",
        blank=True,
        verbose_name="Documents"
    )

    is_public = models.BooleanField(
        default=True,
        verbose_name="Collection publique"
    )

    featured = models.BooleanField(
        default=False,
        verbose_name="Collection mise en avant"
    )

    active = models.BooleanField(
        default=True,
        verbose_name="Active"
    )
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        verbose_name = "Collection"
        verbose_name_plural = "Collections"
        ordering = ["title"]

    def __str__(self):
        return self.title
    # ==========================================================
#              HISTORIQUE DES VERSIONS
# ==========================================================

class DocumentVersion(BaseDocumentModel):
    """
    Historique des différentes versions
    d'un document.

    Permet de conserver toutes les anciennes
    versions afin de pouvoir les consulter
    ou les restaurer.
    """

    document = models.ForeignKey(
        "Document",
        on_delete=models.CASCADE,
        related_name="versions",
        verbose_name="Document"
    )

    version = models.CharField(
        max_length=30,
        verbose_name="Version"
    )

    title = models.CharField(
        max_length=255,
        verbose_name="Titre"
    )

    file = models.FileField(
        upload_to="documents/versions/",
        verbose_name="Fichier"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Description des modifications"
    )

    created_by = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_document_versions",
        verbose_name="Créé par"
    )

    is_current = models.BooleanField(
        default=False,
        verbose_name="Version actuelle"
    )

    class Meta:
        verbose_name = "Version du document"
        verbose_name_plural = "Versions des documents"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.document.title} - {self.version}"
    # ==========================================================
#           NOTIFICATIONS DES DOCUMENTS
# ==========================================================

class DocumentNotification(BaseDocumentModel):
    """
    Notifications liées aux documents.

    Elles permettent d'informer les utilisateurs
    lorsqu'un document est :

    • publié ;
    • modifié ;
    • partagé ;
    • supprimé ;
    • restauré.
    """

    NOTIFICATION_TYPES = [
        ("new", "Nouveau document"),
        ("updated", "Document mis à jour"),
        ("shared", "Document partagé"),
        ("deleted", "Document supprimé"),
        ("restored", "Document restauré"),
        ("other", "Autre"),
    ]

    document = models.ForeignKey(
        "Document",
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name="Document"
    )

    recipient = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.CASCADE,
        related_name="document_notifications",
        verbose_name="Destinataire"
    )

    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default="new",
        verbose_name="Type"
    )

    title = models.CharField(
        max_length=255,
        verbose_name="Titre"
    )

    message = models.TextField(
        verbose_name="Message"
    )

    is_read = models.BooleanField(
        default=False,
        verbose_name="Lu"
    )

    sent_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'envoi"
    )

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ["-sent_at"]

    def __str__(self):
        return f"{self.recipient} - {self.title}"
    # ==========================================================
#            SIGNALEMENT DES DOCUMENTS
# ==========================================================

class DocumentReport(BaseDocumentModel):
    """
    Permet aux utilisateurs de signaler
    un document présentant un problème.

    Les administrateurs pourront ensuite
    consulter ces signalements afin de
    prendre les mesures nécessaires.
    """

    REPORT_TYPES = [
        ("error", "Erreur dans le document"),
        ("duplicate", "Document en double"),
        ("copyright", "Violation de droits d'auteur"),
        ("corrupted", "Fichier corrompu"),
        ("inappropriate", "Contenu inapproprié"),
        ("incorrect", "Informations incorrectes"),
        ("other", "Autre"),
    ]

    STATUS_CHOICES = [
        ("pending", "En attente"),
        ("reviewing", "En cours d'analyse"),
        ("resolved", "Résolu"),
        ("rejected", "Rejeté"),
    ]

    document = models.ForeignKey(
        "Document",
        on_delete=models.CASCADE,
        related_name="reports",
        verbose_name="Document"
    )

    reported_by = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.CASCADE,
        related_name="reported_documents",
        verbose_name="Signalé par"
    )

    report_type = models.CharField(
        max_length=30,
        choices=REPORT_TYPES,
        verbose_name="Type de signalement"
    )

    description = models.TextField(
        verbose_name="Description"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="Statut"
    )

    reviewed_by = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_document_reports",
        verbose_name="Traité par"
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date de traitement"
    )

    admin_note = models.TextField(
        blank=True,
        verbose_name="Note de l'administrateur"
    )

    class Meta:
        verbose_name = "Signalement"
        verbose_name_plural = "Signalements"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.document.title} - {self.get_report_type_display()}"
    # ==========================================================
#            STATISTIQUES DES DOCUMENTS
# ==========================================================

class DocumentStatistic(BaseDocumentModel):
    """
    Statistiques générales d'un document.

    Ce modèle permet de conserver les principales
    statistiques afin d'éviter de recalculer les
    informations à chaque consultation.

    Les valeurs seront mises à jour automatiquement
    par le système.
    """

    document = models.OneToOneField(
        "Document",
        on_delete=models.CASCADE,
        related_name="statistics",
        verbose_name="Document"
    )

    total_views = models.PositiveIntegerField(
        default=0,
        verbose_name="Nombre de consultations"
    )

    total_downloads = models.PositiveIntegerField(
        default=0,
        verbose_name="Nombre de téléchargements"
    )

    total_favorites = models.PositiveIntegerField(
        default=0,
        verbose_name="Nombre de favoris"
    )

    total_comments = models.PositiveIntegerField(
        default=0,
        verbose_name="Nombre de commentaires"
    )

    total_ratings = models.PositiveIntegerField(
        default=0,
        verbose_name="Nombre de notes"
    )

    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        verbose_name="Note moyenne"
    )

    total_shares = models.PositiveIntegerField(
        default=0,
        verbose_name="Nombre de partages"
    )

    total_reports = models.PositiveIntegerField(
        default=0,
        verbose_name="Nombre de signalements"
    )

    last_download = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Dernier téléchargement"
    )

    last_view = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Dernière consultation"
    )

    class Meta:
        verbose_name = "Statistique"
        verbose_name_plural = "Statistiques"
        ordering = ["-total_views"]

    def __str__(self):
        return f"Statistiques - {self.document.title}"