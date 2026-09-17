"""
=============================================================
ESAIE ACADEMY
Application : Library
Fichier : models.py

Bibliothèque Numérique Professionnelle

Développé pour :
    ESAIE ACADEMY

Description
-----------
Cette application gère l'ensemble de la bibliothèque
numérique de la plateforme.

IMPORTANT

Les fichiers physiques (PDF, EPUB, MP4, MP3, DOCX...)
restent gérés par l'application Documents.

Library ajoute uniquement les informations pédagogiques
et bibliographiques.

=============================================================
"""

from uuid import uuid4

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from django.utils.text import slugify
from django.utils import timezone

# ============================================================
# APPLICATIONS DU PROJET
# ============================================================

from documents.models import Document

from configuration.models import SchoolProfile

from subjects.models import Subject

from classes.models import Classe

from teachers.models import Teacher

from students.models import Eleve


# ============================================================
# CONSTANTES
# ============================================================

MAX_TITLE = 255

MAX_SHORT = 100

MAX_MEDIUM = 150

MAX_LONG = 500


# ============================================================
# CHOIX
# ============================================================

class LanguageChoices(models.TextChoices):

    FRENCH = "fr", "Français"

    ENGLISH = "en", "Anglais"

    SPANISH = "es", "Espagnol"

    ARABIC = "ar", "Arabe"

    PORTUGUESE = "pt", "Portugais"

    OTHER = "other", "Autre"


class AccessType(models.TextChoices):

    FREE = "free", "Gratuit"

    PREMIUM = "premium", "Premium"

    SUBSCRIPTION = "subscription", "Abonnement"

    RENT = "rent", "Location"


class ReadingLevel(models.TextChoices):

    PRIMARY = "primary", "Primaire"

    COLLEGE = "college", "Collège"

    HIGH = "high", "Lycée"

    UNIVERSITY = "university", "Université"

    PROFESSIONAL = "professional", "Professionnel"

    GENERAL = "general", "Tout public"


class ResourceType(models.TextChoices):

    BOOK = "book", "Livre"

    MANUAL = "manual", "Manuel"

    EXERCISE = "exercise", "Exercices"

    CORRECTION = "correction", "Corrigé"

    ANNALS = "annals", "Annales"

    MAGAZINE = "magazine", "Magazine"

    ARTICLE = "article", "Article"

    AUDIOBOOK = "audio", "Livre Audio"

    VIDEO = "video", "Vidéo"

    OTHER = "other", "Autre"


# ============================================================
# MODELE ABSTRAIT
# ============================================================

class BaseLibraryModel(models.Model):
    """
    Classe abstraite commune
    à tous les modèles de Library.
    """

    uuid = models.UUIDField(
        default=uuid4,
        editable=False,
        unique=True,
    )

    active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="Actif",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_created",
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_updated",
    )

    observations = models.TextField(
        blank=True,
    )

    class Meta:

        abstract = True

        ordering = ["-created_at"]


# ============================================================
# CATEGORIES
# ============================================================

class LibraryCategory(BaseLibraryModel):
    """
    Catégories de la bibliothèque.
    """

    name = models.CharField(
        max_length=120,
        unique=True,
        db_index=True,
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
    )

    color = models.CharField(
        max_length=20,
        default="#198754",
    )

    image = models.ImageField(
        upload_to="library/categories/",
        blank=True,
        null=True,
    )

    order = models.PositiveIntegerField(
        default=0,
    )

    class Meta:

        verbose_name = "Catégorie"

        verbose_name_plural = "Catégories"

        ordering = ["order", "name"]

    def save(self, *args, **kwargs):

        if not self.slug:

            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):

        return self.name
    

    # ============================================================
# AUTEURS
# ============================================================

class LibraryAuthor(BaseLibraryModel):
    """
    Représente un auteur de ressources pédagogiques.

    Un auteur peut avoir plusieurs ouvrages dans la
    bibliothèque numérique.
    """

    first_name = models.CharField(
        max_length=100,
        verbose_name="Prénom",
    )

    last_name = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name="Nom",
    )

    photo = models.ImageField(
        upload_to="library/authors/",
        blank=True,
        null=True,
        verbose_name="Photo",
    )

    biography = models.TextField(
        blank=True,
        verbose_name="Biographie",
    )

    nationality = models.CharField(
        max_length=100,
        blank=True,
    )

    birth_date = models.DateField(
        blank=True,
        null=True,
    )

    death_date = models.DateField(
        blank=True,
        null=True,
    )

    email = models.EmailField(
        blank=True,
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
    )

    website = models.URLField(
        blank=True,
    )

    facebook = models.URLField(blank=True)

    linkedin = models.URLField(blank=True)

    twitter = models.URLField(blank=True)

    photo_copyright = models.CharField(
        max_length=255,
        blank=True,
    )

    verified = models.BooleanField(
        default=False,
    )

    featured = models.BooleanField(
        default=False,
    )

    class Meta:

        ordering = [
            "last_name",
            "first_name"
        ]

        verbose_name = "Auteur"

        verbose_name_plural = "Auteurs"

        indexes = [

            models.Index(fields=["last_name"]),

            models.Index(fields=["verified"]),

            models.Index(fields=["featured"]),

        ]

    @property
    def full_name(self):

        return f"{self.first_name} {self.last_name}"

    @property
    def total_books(self):

        return self.books.count()

    def __str__(self):

        return self.full_name
    # ============================================================
# EDITEURS
# ============================================================

class LibraryPublisher(BaseLibraryModel):
    """
    Maison d'édition.
    """

    name = models.CharField(
        max_length=200,
        unique=True,
    )

    logo = models.ImageField(
        upload_to="library/publishers/",
        blank=True,
        null=True,
    )

    description = models.TextField(
        blank=True,
    )

    country = models.CharField(
        max_length=100,
        blank=True,
    )

    city = models.CharField(
        max_length=100,
        blank=True,
    )

    address = models.TextField(
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
    )

    website = models.URLField(
        blank=True,
    )

    active_contract = models.BooleanField(
        default=False,
    )

    verified = models.BooleanField(
        default=False,
    )

    class Meta:

        verbose_name = "Éditeur"

        verbose_name_plural = "Éditeurs"

        ordering = [
            "name"
        ]

    def __str__(self):

        return self.name
    # ============================================================
# COLLECTIONS
# ============================================================

class LibraryCollection(BaseLibraryModel):
    """
    Collection pédagogique.

    Exemple :

    Préparation BEPC

    Préparation BAC D

    Mathématiques 6ème

    Sciences expérimentales

    Concours ENS
    """

    title = models.CharField(
        max_length=255,
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    cover = models.ImageField(
        upload_to="library/collections/",
        blank=True,
        null=True,
    )

    school = models.ForeignKey(
        SchoolProfile,
        on_delete=models.CASCADE,
        related_name="library_collections",
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="library_collections",
    )

    classe = models.ForeignKey(
        Classe,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="library_collections",
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_library_collections",
    )

    public = models.BooleanField(
        default=True,
    )

    featured = models.BooleanField(
        default=False,
    )

    class Meta:

        verbose_name = "Collection"

        verbose_name_plural = "Collections"

        ordering = [
            "title"
        ]

    def save(self, *args, **kwargs):

        if not self.slug:

            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    @property
    def total_books(self):

        return self.books.count()

    def __str__(self):

        return self.title
    # ============================================================
# LIVRES
# ============================================================

class LibraryBook(BaseLibraryModel):
    """
    ===========================================================
    LIVRE PEDAGOGIQUE

    Ce modèle représente un ouvrage de la bibliothèque.

    IMPORTANT

    Les fichiers (PDF, EPUB, DOCX, MP4...)

    sont gérés par l'application DOCUMENTS.

    Library ajoute uniquement les informations
    bibliographiques et pédagogiques.

    ===========================================================
    """

    # ---------------------------------------------------------
    # DOCUMENT PRINCIPAL
    # ---------------------------------------------------------

    document = models.OneToOneField(
        Document,
        on_delete=models.CASCADE,
        related_name="library_book",
        verbose_name="Document",
    )

    # ---------------------------------------------------------
    # IDENTIFICATION
    # ---------------------------------------------------------

    title = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name="Titre",
    )

    subtitle = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Sous titre",
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
    )

    short_description = models.TextField(
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    summary = models.TextField(
        blank=True,
        verbose_name="Résumé",
    )

    isbn = models.CharField(
        max_length=30,
        blank=True,
        db_index=True,
    )

    doi = models.CharField(
        max_length=100,
        blank=True,
    )

    edition_name = models.CharField(
        max_length=100,
        blank=True,
    )

    language = models.CharField(
        max_length=20,
        choices=LanguageChoices.choices,
        default=LanguageChoices.FRENCH,
    )

    resource_type = models.CharField(
        max_length=30,
        choices=ResourceType.choices,
        default=ResourceType.BOOK,
    )

    reading_level = models.CharField(
        max_length=30,
        choices=ReadingLevel.choices,
        default=ReadingLevel.COLLEGE,
    )

    access_type = models.CharField(
        max_length=30,
        choices=AccessType.choices,
        default=AccessType.FREE,
    )

    # ---------------------------------------------------------
    # RELATIONS
    # ---------------------------------------------------------

    school = models.ForeignKey(
        SchoolProfile,
        on_delete=models.CASCADE,
        related_name="library_books",
    )

    category = models.ForeignKey(
        LibraryCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="books",
    )

    publisher = models.ForeignKey(
        LibraryPublisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="books",
    )

    collection = models.ForeignKey(
        LibraryCollection,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="books",
    )

    authors = models.ManyToManyField(
        LibraryAuthor,
        related_name="books",
        blank=True,
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="library_books",
    )

    classe = models.ForeignKey(
        Classe,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="library_books",
    )

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="published_library_books",
    )

    # ---------------------------------------------------------
    # INFORMATIONS PEDAGOGIQUES
    # ---------------------------------------------------------

    objectives = models.TextField(
        blank=True,
    )

    prerequisites = models.TextField(
        blank=True,
    )

    competencies = models.TextField(
        blank=True,
    )

    keywords = models.TextField(
        blank=True,
    )

    program_reference = models.CharField(
        max_length=255,
        blank=True,
    )

    academic_year = models.CharField(
        max_length=30,
        blank=True,
    )

    recommended_age = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    estimated_reading_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    page_count = models.PositiveIntegerField(
        default=0,
    )

    chapter_count = models.PositiveIntegerField(
        default=0,
    )

    word_count = models.PositiveIntegerField(
        default=0,
    )

    publication_year = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    publication_date = models.DateField(
        null=True,
        blank=True,
    )
        # ==========================================================
    # DROITS D'ACCES
    # ==========================================================

    is_public = models.BooleanField(
        default=True,
        verbose_name="Visible par tous"
    )

    is_featured = models.BooleanField(
        default=False,
        verbose_name="Livre recommandé"
    )

    is_published = models.BooleanField(
        default=True,
        verbose_name="Publié"
    )

    is_premium = models.BooleanField(
        default=False,
        verbose_name="Premium"
    )

    allow_download = models.BooleanField(
        default=True,
        verbose_name="Téléchargement autorisé"
    )

    allow_online_reading = models.BooleanField(
        default=True,
        verbose_name="Lecture en ligne"
    )

    allow_print = models.BooleanField(
        default=False,
        verbose_name="Impression autorisée"
    )

    allow_share = models.BooleanField(
        default=False,
        verbose_name="Partage autorisé"
    )

    allow_copy = models.BooleanField(
        default=False,
        verbose_name="Copie autorisée"
    )

    allow_comment = models.BooleanField(
        default=True,
        verbose_name="Commentaires autorisés"
    )

    allow_rating = models.BooleanField(
        default=True,
        verbose_name="Notation autorisée"
    )

    downloadable_only_for_premium = models.BooleanField(
        default=False
    )

    # ==========================================================
    # TARIFICATION
    # ==========================================================

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    old_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    subscription_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    rental_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    currency = models.CharField(
        max_length=10,
        default="XOF"
    )

    # ==========================================================
    # STATISTIQUES
    # ==========================================================

    total_views = models.PositiveBigIntegerField(
        default=0
    )

    total_downloads = models.PositiveBigIntegerField(
        default=0
    )

    total_reads = models.PositiveBigIntegerField(
        default=0
    )

    total_favorites = models.PositiveBigIntegerField(
        default=0
    )

    total_comments = models.PositiveBigIntegerField(
        default=0
    )

    total_ratings = models.PositiveBigIntegerField(
        default=0
    )

    average_rating = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0
    )

    total_shares = models.PositiveIntegerField(
        default=0
    )

    total_reports = models.PositiveIntegerField(
        default=0
    )

    # ==========================================================
    # SEO
    # ==========================================================

    meta_title = models.CharField(
        max_length=255,
        blank=True
    )

    meta_description = models.TextField(
        blank=True
    )

    meta_keywords = models.TextField(
        blank=True
    )

    canonical_url = models.URLField(
        blank=True
    )

    # ==========================================================
    # IA
    # ==========================================================

    ai_summary = models.TextField(
        blank=True
    )

    ai_keywords = models.TextField(
        blank=True
    )

    ai_recommendation = models.TextField(
        blank=True
    )

    ai_difficulty_score = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0
    )

    ai_quality_score = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0
    )

    ai_generated = models.BooleanField(
        default=False
    )

    # ==========================================================
    # ARCHIVAGE
    # ==========================================================

    archived = models.BooleanField(
        default=False
    )

    archived_at = models.DateTimeField(
        null=True,
        blank=True
    )

    archived_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="archived_library_books"
    )
        # ==========================================================
    # PROPRIÉTÉS
    # ==========================================================

    @property
    def is_free(self):
        """Retourne True si le livre est gratuit."""
        return not self.is_premium and self.price == 0

    @property
    def is_paid(self):
        """Retourne True si le livre est payant."""
        return self.is_premium or self.price > 0

    @property
    def can_be_downloaded(self):
        """Autorisation de téléchargement."""
        return self.allow_download and self.is_published and self.active

    @property
    def can_be_read_online(self):
        """Lecture en ligne."""
        return self.allow_online_reading and self.active

    @property
    def is_available(self):
        """Livre disponible."""
        return (
            self.active
            and self.is_published
            and not self.archived
        )

    @property
    def popularity_score(self):
        """
        Calcul simple de popularité.
        """

        return (
            self.total_views +
            (self.total_downloads * 5) +
            (self.total_favorites * 10) +
            (self.total_reads * 2)
        )

    @property
    def complete_title(self):
        if self.subtitle:
            return f"{self.title} : {self.subtitle}"
        return self.title

    @property
    def author_names(self):
        return ", ".join(
            self.authors.values_list(
                "last_name",
                flat=True
            )
        )

    # ==========================================================
    # METHODES
    # ==========================================================

    def publish(self):

        self.is_published = True

        self.save(
            update_fields=["is_published"]
        )

    def unpublish(self):

        self.is_published = False

        self.save(
            update_fields=["is_published"]
        )

    def archive(self, user=None):

        self.archived = True

        self.archived_at = timezone.now()

        self.archived_by = user

        self.save()

    def restore(self):

        self.archived = False

        self.archived_at = None

        self.archived_by = None

        self.save()

    def increment_views(self):

        self.total_views += 1

        self.save(update_fields=["total_views"])

    def increment_downloads(self):

        self.total_downloads += 1

        self.save(update_fields=["total_downloads"])

    def increment_reads(self):

        self.total_reads += 1

        self.save(update_fields=["total_reads"])

    def increment_favorites(self):

        self.total_favorites += 1

        self.save(update_fields=["total_favorites"])

    def update_rating(self, rating):

        total = (
            self.average_rating *
            self.total_ratings
        ) + rating

        self.total_ratings += 1

        self.average_rating = (
            total / self.total_ratings
        )

        self.save(
            update_fields=[
                "average_rating",
                "total_ratings"
            ]
        )

    # ==========================================================
    # SAVE
    # ==========================================================

    def save(self, *args, **kwargs):

        if not self.slug:

            self.slug = slugify(self.title)

        if not self.meta_title:

            self.meta_title = self.title

        if (
            not self.meta_description
            and self.summary
        ):
            self.meta_description = self.summary[:160]

        super().save(*args, **kwargs)

    # ==========================================================
    # META
    # ==========================================================

    class Meta:

        verbose_name = "Livre"

        verbose_name_plural = "Livres"

        ordering = [
            "-created_at",
            "title"
        ]

        indexes = [

            models.Index(fields=["title"]),

            models.Index(fields=["isbn"]),

            models.Index(fields=["slug"]),

            models.Index(fields=["language"]),

            models.Index(fields=["resource_type"]),

            models.Index(fields=["reading_level"]),

            models.Index(fields=["is_public"]),

            models.Index(fields=["is_published"]),

            models.Index(fields=["is_premium"]),

            models.Index(fields=["publication_year"]),

            models.Index(fields=["total_views"]),

            models.Index(fields=["total_downloads"]),

            models.Index(fields=["average_rating"]),

            models.Index(fields=["created_at"]),

        ]

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "document"
                ],
                name="unique_library_document"
            ),

            models.UniqueConstraint(
                fields=[
                    "title",
                    "edition_name",
                    "publication_year"
                ],
                name="unique_library_book"
            )

        ]

    # ==========================================================
    # STRING
    # ==========================================================

    def __str__(self):

        return self.complete_title
    # ==========================================================
# EDITIONS
# ==========================================================

class LibraryEdition(BaseLibraryModel):
    """
    Représente une édition d'un livre.

    Un même livre peut posséder plusieurs éditions.
    """

    book = models.ForeignKey(
        LibraryBook,
        on_delete=models.CASCADE,
        related_name="editions"
    )

    document = models.OneToOneField(
        Document,
        on_delete=models.CASCADE,
        related_name="library_edition",
        null=True,
        blank=True
    )

    edition_name = models.CharField(
        max_length=150
    )

    edition_number = models.PositiveIntegerField(
        default=1
    )

    isbn = models.CharField(
        max_length=30,
        blank=True
    )

    publication_year = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    publication_date = models.DateField(
        null=True,
        blank=True
    )

    language = models.CharField(
        max_length=20,
        choices=LanguageChoices.choices,
        default=LanguageChoices.FRENCH
    )

    page_count = models.PositiveIntegerField(
        default=0
    )

    revision = models.CharField(
        max_length=100,
        blank=True
    )

    version = models.CharField(
        max_length=50,
        blank=True
    )

    available = models.BooleanField(
        default=True
    )

    is_latest = models.BooleanField(
        default=False
    )

    notes = models.TextField(
        blank=True
    )

    class Meta:

        ordering = [
            "-publication_year",
            "-edition_number"
        ]

        verbose_name = "Edition"

        verbose_name_plural = "Editions"

        indexes = [

            models.Index(fields=["publication_year"]),

            models.Index(fields=["edition_number"]),

            models.Index(fields=["is_latest"]),

        ]

    @property
    def display_name(self):

        return f"{self.book.title} ({self.edition_name})"

    def __str__(self):

        return self.display_name
    # ==========================================================
# CHAPITRES
# ==========================================================

class LibraryChapter(BaseLibraryModel):
    """
    ==========================================================

    CHAPITRE D'UN LIVRE

    Chaque chapitre est une unité pédagogique.

    Il peut contenir :

    - texte
    - vidéo
    - PDF
    - images
    - exercices
    - corrigés
    - quiz
    - liens externes
    - compétences
    - durée de lecture

    ==========================================================
    """

    # ------------------------------------------------------
    # RELATIONS
    # ------------------------------------------------------

    book = models.ForeignKey(
        LibraryBook,
        on_delete=models.CASCADE,
        related_name="chapters",
        verbose_name="Livre",
    )

    document = models.ForeignKey(
        Document,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="library_chapters",
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )

    # ------------------------------------------------------
    # IDENTIFICATION
    # ------------------------------------------------------

    title = models.CharField(
        max_length=255,
    )

    slug = models.SlugField(
        blank=True,
    )

    chapter_number = models.PositiveIntegerField(
        default=1,
    )

    order = models.PositiveIntegerField(
        default=1,
    )

    short_description = models.TextField(
        blank=True,
    )

    content = models.TextField(
        blank=True,
    )

    summary = models.TextField(
        blank=True,
    )

    objectives = models.TextField(
        blank=True,
    )

    competencies = models.TextField(
        blank=True,
    )

    prerequisites = models.TextField(
        blank=True,
    )

    keywords = models.TextField(
        blank=True,
    )

    # ------------------------------------------------------
    # PEDAGOGIE
    # ------------------------------------------------------

    estimated_minutes = models.PositiveIntegerField(
        default=30,
    )

    difficulty = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )

    page_start = models.PositiveIntegerField(
        default=1,
    )

    page_end = models.PositiveIntegerField(
        default=1,
    )

    exercise_count = models.PositiveIntegerField(
        default=0,
    )

    quiz_count = models.PositiveIntegerField(
        default=0,
    )

    practical_work_count = models.PositiveIntegerField(
        default=0,
    )

    # ------------------------------------------------------
    # CONTENU
    # ------------------------------------------------------

    has_video = models.BooleanField(
        default=False,
    )

    has_audio = models.BooleanField(
        default=False,
    )

    has_pdf = models.BooleanField(
        default=False,
    )

    has_images = models.BooleanField(
        default=False,
    )

    has_quiz = models.BooleanField(
        default=False,
    )

    has_exercises = models.BooleanField(
        default=False,
    )

    has_correction = models.BooleanField(
        default=False,
    )

    # ------------------------------------------------------
    # VISIBILITE
    # ------------------------------------------------------

    is_published = models.BooleanField(
        default=True,
    )

    is_free = models.BooleanField(
        default=True,
    )

    is_preview = models.BooleanField(
        default=False,
    )

    active = models.BooleanField(
        default=True,
    )

    # ------------------------------------------------------
    # STATISTIQUES
    # ------------------------------------------------------

    total_views = models.PositiveIntegerField(
        default=0,
    )

    total_reads = models.PositiveIntegerField(
        default=0,
    )

    total_downloads = models.PositiveIntegerField(
        default=0,
    )

    average_completion = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    average_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    # ------------------------------------------------------
    # IA
    # ------------------------------------------------------

    ai_summary = models.TextField(
        blank=True,
    )

    ai_keywords = models.TextField(
        blank=True,
    )

    ai_generated_questions = models.TextField(
        blank=True,
    )

    ai_revision_sheet = models.TextField(
        blank=True,
    )

    ai_difficulty = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0,
    )

    # ------------------------------------------------------
    # METHODES
    # ------------------------------------------------------

    @property
    def total_pages(self):

        return (
            self.page_end -
            self.page_start
        ) + 1

    @property
    def is_root(self):

        return self.parent is None

    @property
    def children_count(self):

        return self.children.count()

    def save(self, *args, **kwargs):

        if not self.slug:

            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    class Meta:

        verbose_name = "Chapitre"

        verbose_name_plural = "Chapitres"

        ordering = [
            "chapter_number",
            "order"
        ]

        indexes = [

            models.Index(
                fields=[
                    "chapter_number"
                ]
            ),

            models.Index(
                fields=[
                    "order"
                ]
            ),

            models.Index(
                fields=[
                    "is_published"
                ]
            ),

            models.Index(
                fields=[
                    "is_free"
                ]
            ),

        ]

    def __str__(self):

        return f"Chapitre {self.chapter_number} - {self.title}"
    # ==========================================================
# SIGNETS
# ==========================================================

class LibraryBookmark(BaseLibraryModel):
    """
    Signet personnel.

    Permet à un utilisateur de retrouver rapidement
    une page ou un chapitre.
    """

    Eleve = models.ForeignKey(
        Eleve,
        on_delete=models.CASCADE,
        related_name="library_bookmarks"
    )

    book = models.ForeignKey(
        LibraryBook,
        on_delete=models.CASCADE,
        related_name="bookmarks"
    )

    chapter = models.ForeignKey(
        LibraryChapter,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookmarks"
    )

    page = models.PositiveIntegerField(
        default=1
    )

    note = models.TextField(
        blank=True
    )

    color = models.CharField(
        max_length=20,
        default="#ffc107"
    )

    icon = models.CharField(
        max_length=50,
        default="bookmark"
    )

    class Meta:

        verbose_name = "Signet"

        verbose_name_plural = "Signets"

        ordering = [
            "-created_at"
        ]

        unique_together = (
            "Eleve",
            "book",
            "page",
        )

    def __str__(self):

        return f"{self.Eleve} - {self.book}"
    # ==========================================================
# PROGRESSION DE LECTURE
# ==========================================================

class LibraryReadingProgress(BaseLibraryModel):
    """
    Sauvegarde automatique
    de la progression de lecture.
    """

    Eleve = models.ForeignKey(
        Eleve,
        on_delete=models.CASCADE,
        related_name="reading_progress"
    )

    book = models.ForeignKey(
        LibraryBook,
        on_delete=models.CASCADE,
        related_name="reading_progress"
    )

    current_chapter = models.ForeignKey(
        LibraryChapter,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    current_page = models.PositiveIntegerField(
        default=1
    )

    last_page = models.PositiveIntegerField(
        default=1
    )

    completion_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    minutes_read = models.PositiveIntegerField(
        default=0
    )

    sessions = models.PositiveIntegerField(
        default=0
    )

    completed = models.BooleanField(
        default=False
    )

    last_read = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        verbose_name = "Progression"

        verbose_name_plural = "Progressions"

        unique_together = (
            "Eleve",
            "book",
        )

    @property
    def remaining_percentage(self):

        return 100 - self.completion_percentage

    def __str__(self):

        return f"{self.Eleve} - {self.book}"
    # ==========================================================
# HISTORIQUE
# ==========================================================

class LibraryHistory(BaseLibraryModel):
    """
    Historique complet
    des lectures.
    """

    Eleve = models.ForeignKey(
        Eleve,
        on_delete=models.CASCADE,
        related_name="library_history"
    )

    book = models.ForeignKey(
        LibraryBook,
        on_delete=models.CASCADE,
        related_name="history"
    )

    chapter = models.ForeignKey(
        LibraryChapter,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    action = models.CharField(
        max_length=100,
        choices=[
            ("open", "Ouverture"),
            ("read", "Lecture"),
            ("download", "Téléchargement"),
            ("favorite", "Favori"),
            ("finish", "Terminé"),
        ]
    )

    page = models.PositiveIntegerField(
        default=1
    )

    duration = models.PositiveIntegerField(
        default=0,
        help_text="Durée en secondes"
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    device = models.CharField(
        max_length=150,
        blank=True
    )

    browser = models.CharField(
        max_length=150,
        blank=True
    )

    class Meta:

        verbose_name = "Historique"

        verbose_name_plural = "Historiques"

        ordering = [
            "-created_at"
        ]

    def __str__(self):

        return f"{self.Eleve} - {self.action}"
    # ==========================================================
# FAVORIS
# ==========================================================

class LibraryFavorite(BaseLibraryModel):
    """
    Livres favoris d'un utilisateur.
    """

    Eleve = models.ForeignKey(
        Eleve,
        on_delete=models.CASCADE,
        related_name="library_favorites"
    )

    book = models.ForeignKey(
        LibraryBook,
        on_delete=models.CASCADE,
        related_name="favorites"
    )

    class Meta:

        verbose_name = "Favori"

        verbose_name_plural = "Favoris"

        unique_together = (
            "Eleve",
            "book",
        )

    def __str__(self):

        return f"{self.Eleve} ❤️ {self.book}"


# ==========================================================
# NOTES
# ==========================================================

class LibraryRating(BaseLibraryModel):
    """
    Note attribuée à un livre.
    """

    Eleve = models.ForeignKey(
        Eleve,
        on_delete=models.CASCADE,
        related_name="library_ratings"
    )

    book = models.ForeignKey(
        LibraryBook,
        on_delete=models.CASCADE,
        related_name="ratings"
    )

    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )

    class Meta:

        verbose_name = "Note"

        verbose_name_plural = "Notes"

        unique_together = (
            "Eleve",
            "book",
        )

    def __str__(self):

        return f"{self.book} ({self.rating}/5)"


# ==========================================================
# AVIS
# ==========================================================

class LibraryReview(BaseLibraryModel):
    """
    Avis laissé par un lecteur.
    """

    Eleve = models.ForeignKey(
        Eleve,
        on_delete=models.CASCADE,
        related_name="library_reviews"
    )

    book = models.ForeignKey(
        LibraryBook,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    title = models.CharField(
        max_length=200
    )

    review = models.TextField()

    approved = models.BooleanField(
        default=False
    )

    reported = models.BooleanField(
        default=False
    )

    likes = models.PositiveIntegerField(
        default=0
    )

    dislikes = models.PositiveIntegerField(
        default=0
    )

    class Meta:

        ordering = [
            "-created_at"
        ]

        verbose_name = "Avis"

        verbose_name_plural = "Avis"

    def __str__(self):

        return self.title


# ==========================================================
# EMPRUNTS
# ==========================================================

class LibraryBorrow(BaseLibraryModel):
    """
    Gestion des emprunts numériques.
    """

    Eleve = models.ForeignKey(
        Eleve,
        on_delete=models.CASCADE,
        related_name="library_borrows"
    )

    book = models.ForeignKey(
        LibraryBook,
        on_delete=models.CASCADE,
        related_name="borrows"
    )

    borrow_date = models.DateTimeField(
        auto_now_add=True
    )

    due_date = models.DateTimeField()

    return_date = models.DateTimeField(
        null=True,
        blank=True
    )

    renewed = models.BooleanField(
        default=False
    )

    completed = models.BooleanField(
        default=False
    )

    class Meta:

        verbose_name = "Emprunt"

        verbose_name_plural = "Emprunts"

        ordering = [
            "-borrow_date"
        ]

    @property
    def is_late(self):

        if self.completed:
            return False

        return timezone.now() > self.due_date

    def __str__(self):

        return f"{self.Eleve} → {self.book}"


# ==========================================================
# RESERVATIONS
# ==========================================================

class LibraryReservation(BaseLibraryModel):
    """
    Réservation d'un livre.
    """

    Eleve = models.ForeignKey(
        Eleve,
        on_delete=models.CASCADE,
        related_name="library_reservations"
    )

    book = models.ForeignKey(
        LibraryBook,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    reservation_date = models.DateTimeField(
        auto_now_add=True
    )

    expiration_date = models.DateTimeField()

    active = models.BooleanField(
        default=True
    )

    notified = models.BooleanField(
        default=False
    )

    class Meta:

        verbose_name = "Réservation"

        verbose_name_plural = "Réservations"

        ordering = [
            "-reservation_date"
        ]

    def __str__(self):

        return f"{self.Eleve} → {self.book}"
    # ==========================================================
# TELECHARGEMENTS
# ==========================================================

class LibraryDownload(BaseLibraryModel):
    """
    Historique complet des téléchargements.
    """

    Eleve = models.ForeignKey(
        Eleve,
        on_delete=models.CASCADE,
        related_name="library_downloads"
    )

    book = models.ForeignKey(
        LibraryBook,
        on_delete=models.CASCADE,
        related_name="downloads"
    )

    chapter = models.ForeignKey(
        LibraryChapter,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="downloads"
    )

    download_date = models.DateTimeField(
        auto_now_add=True
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    device = models.CharField(
        max_length=120,
        blank=True
    )

    browser = models.CharField(
        max_length=120,
        blank=True
    )

    downloaded_file = models.CharField(
        max_length=255,
        blank=True
    )

    class Meta:

        ordering = [
            "-download_date"
        ]

        verbose_name = "Téléchargement"

        verbose_name_plural = "Téléchargements"

    def __str__(self):

        return f"{self.Eleve} - {self.book}"
    # ==========================================================
# ANNOTATIONS
# ==========================================================

class LibraryAnnotation(BaseLibraryModel):
    """
    Notes personnelles d'un étudiant.
    """

    Eleve = models.ForeignKey(
        Eleve,
        on_delete=models.CASCADE,
        related_name="library_annotations"
    )

    book = models.ForeignKey(
        LibraryBook,
        on_delete=models.CASCADE,
        related_name="annotations"
    )

    chapter = models.ForeignKey(
        LibraryChapter,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    page = models.PositiveIntegerField()

    selected_text = models.TextField()

    note = models.TextField(
        blank=True
    )

    color = models.CharField(
        max_length=30,
        default="#ffff00"
    )

    class Meta:

        verbose_name = "Annotation"

        verbose_name_plural = "Annotations"

    def __str__(self):

        return self.selected_text[:40]
    # ==========================================================
# CITATIONS
# ==========================================================

class LibraryQuote(BaseLibraryModel):

    Eleve = models.ForeignKey(
        Eleve,
        on_delete=models.CASCADE,
        related_name="library_quotes"
    )

    book = models.ForeignKey(
        LibraryBook,
        on_delete=models.CASCADE,
        related_name="quotes"
    )

    page = models.PositiveIntegerField()

    quote = models.TextField()

    class Meta:

        verbose_name = "Citation"

        verbose_name_plural = "Citations"

    def __str__(self):

        return self.quote[:50]
    # ==========================================================
# CERTIFICATS
# ==========================================================

class LibraryCertificate(BaseLibraryModel):
    """
    Certificat obtenu après
    lecture complète d'un parcours.
    """

    Eleve = models.ForeignKey(
        Eleve,
        on_delete=models.CASCADE,
        related_name="library_certificates"
    )

    book = models.ForeignKey(
        LibraryBook,
        on_delete=models.CASCADE,
        related_name="certificates"
    )

    certificate_number = models.CharField(
        max_length=100,
        unique=True
    )

    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    issue_date = models.DateTimeField(
        auto_now_add=True
    )

    pdf_generated = models.BooleanField(
        default=False
    )

    class Meta:

        verbose_name = "Certificat"

        verbose_name_plural = "Certificats"

    def __str__(self):

        return self.certificate_number
    # ==========================================================
# RECOMMANDATIONS IA
# ==========================================================

class LibraryRecommendation(BaseLibraryModel):
    """
    Recommandations personnalisées.
    """

    Eleve = models.ForeignKey(
        Eleve,
        on_delete=models.CASCADE,
        related_name="library_recommendations"
    )

    recommended_book = models.ForeignKey(
        LibraryBook,
        on_delete=models.CASCADE,
        related_name="recommended_to"
    )

    confidence = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    reason = models.TextField(
        blank=True
    )

    accepted = models.BooleanField(
        default=False
    )

    class Meta:

        verbose_name = "Recommandation"

        verbose_name_plural = "Recommandations"

    def __str__(self):

        return f"{self.Eleve}"
    # ==========================================================
# STATISTIQUES
# ==========================================================

class LibraryStatistics(BaseLibraryModel):

    book = models.OneToOneField(
        LibraryBook,
        on_delete=models.CASCADE,
        related_name="statistics"
    )

    total_Eleves = models.PositiveIntegerField(
        default=0
    )

    completed_Eleves = models.PositiveIntegerField(
        default=0
    )

    average_progress = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    average_reading_time = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    average_rating = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0
    )

    success_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    class Meta:

        verbose_name = "Statistique"

        verbose_name_plural = "Statistiques"

    def __str__(self):

        return self.book.title
    """
==============================================================

ESAIE ACADEMY

Application : Library

Managers personnalisés

==============================================================
"""

from django.db import models
from django.db.models import Avg
from django.db.models import Count
from django.db.models import Q
from django.utils import timezone


# ============================================================
# BOOK QUERYSET
# ============================================================

class LibraryBookQuerySet(models.QuerySet):

    def active(self):
        return self.filter(active=True)

    def published(self):
        return self.filter(is_published=True)

    def available(self):
        return self.filter(
            active=True,
            is_published=True,
            archived=False
        )

    def archived(self):
        return self.filter(
            archived=True
        )

    def premium(self):
        return self.filter(
            is_premium=True
        )

    def free_books(self):
        return self.filter(
            is_premium=False
        )

    def public(self):
        return self.filter(
            is_public=True
        )

    def featured(self):
        return self.filter(
            is_featured=True
        )

    def latest(self):

        return self.order_by(
            "-created_at"
        )

    def most_downloaded(self):

        return self.order_by(
            "-total_downloads"
        )

    def most_read(self):

        return self.order_by(
            "-total_reads"
        )

    def popular(self):

        return self.order_by(
            "-total_views"
        )

    def best_rated(self):

        return self.order_by(
            "-average_rating"
        )

    def french(self):

        return self.filter(
            language="fr"
        )

    def english(self):

        return self.filter(
            language="en"
        )

    def books(self):

        return self.filter(
            resource_type="book"
        )

    def manuals(self):

        return self.filter(
            resource_type="manual"
        )

    def videos(self):

        return self.filter(
            resource_type="video"
        )

    def audiobooks(self):

        return self.filter(
            resource_type="audio"
        )

    def by_subject(self, subject):

        return self.filter(
            subject=subject
        )

    def by_class(self, classe):

        return self.filter(
            classe=classe
        )

    def by_teacher(self, teacher):

        return self.filter(
            teacher=teacher
        )

    def by_category(self, category):

        return self.filter(
            category=category
        )

    def by_publisher(self, publisher):

        return self.filter(
            publisher=publisher
        )

    def published_this_year(self):

        return self.filter(
            publication_year=timezone.now().year
        )

    def search(self, text):

        return self.filter(

            Q(title__icontains=text)

            |

            Q(subtitle__icontains=text)

            |

            Q(summary__icontains=text)

            |

            Q(keywords__icontains=text)

        )

    def recommended(self):

        return self.available()\
            .featured()\
            .best_rated()

# ============================================================
# BOOK MANAGER
# ============================================================

class LibraryBookManager(models.Manager):

    def get_queryset(self):
        return LibraryBookQuerySet(
            self.model,
            using=self._db
        )

    def active(self):
        return self.get_queryset().active()

    def available(self):
        return self.get_queryset().available()

    def published(self):
        return self.get_queryset().published()

    def archived(self):
        return self.get_queryset().archived()

    def premium(self):
        return self.get_queryset().premium()

    def free_books(self):
        return self.get_queryset().free_books()

    def public(self):
        return self.get_queryset().public()

    def featured(self):
        return self.get_queryset().featured()

    def latest(self):
        return self.get_queryset().latest()

    def popular(self):
        return self.get_queryset().popular()

    def best_rated(self):
        return self.get_queryset().best_rated()

    def most_downloaded(self):
        return self.get_queryset().most_downloaded()

    def most_read(self):
        return self.get_queryset().most_read()

    def search(self, text):
        return self.get_queryset().search(text)

    def recommended(self):
        return self.get_queryset().recommended()

    def by_subject(self, subject):
        return self.get_queryset().by_subject(subject)

    def by_class(self, classe):
        return self.get_queryset().by_class(classe)

    def by_teacher(self, teacher):
        return self.get_queryset().by_teacher(teacher)

    def by_category(self, category):
        return self.get_queryset().by_category(category)

    def by_publisher(self, publisher):
        return self.get_queryset().by_publisher(publisher)

    def statistics(self):
        return self.aggregate(
            total=models.Count("id"),
            downloads=models.Sum("total_downloads"),
            reads=models.Sum("total_reads"),
            views=models.Sum("total_views"),
            average_rating=models.Avg("average_rating"),
        )


"""
=========================================================
ESAIE ACADEMY

Application : Library

Services Métier
=========================================================
"""

from django.db import transaction
from django.utils import timezone

from .models import (
    LibraryBook,
    LibraryBorrow,
    LibraryReservation,
    LibraryDownload,
    LibraryReadingProgress,
    LibraryHistory,
    LibraryFavorite,
    LibraryRating,
    LibraryReview,
    LibraryCertificate,
    LibraryStatistics,
)


class LibraryService:
    """
    Service principal de la bibliothèque.
    Toute la logique métier passe par cette classe.
    """

    # ======================================================
    # EMPRUNTS
    # ======================================================

    @staticmethod
    @transaction.atomic
    def borrow_book(student, book, due_date):

        borrow = LibraryBorrow.objects.create(
            student=student,
            book=book,
            due_date=due_date,
        )

        return borrow

    @staticmethod
    @transaction.atomic
    def return_book(borrow):

        borrow.completed = True
        borrow.return_date = timezone.now()
        borrow.save()

        return borrow

    # ======================================================
    # RESERVATIONS
    # ======================================================

    @staticmethod
    @transaction.atomic
    def reserve_book(student, book, expiration):

        reservation = LibraryReservation.objects.create(
            student=student,
            book=book,
            expiration_date=expiration,
        )

        return reservation

    # ======================================================
    # TELECHARGEMENTS
    # ======================================================

    @staticmethod
    @transaction.atomic
    def register_download(student, book, request=None):

        LibraryDownload.objects.create(
            student=student,
            book=book,
            ip_address=request.META.get("REMOTE_ADDR") if request else None,
        )

        book.increment_downloads()

        return True

    # ======================================================
    # HISTORIQUE
    # ======================================================

    @staticmethod
    def register_history(
        student,
        book,
        action,
        chapter=None,
        page=1,
    ):

        return LibraryHistory.objects.create(
            student=student,
            book=book,
            chapter=chapter,
            action=action,
            page=page,
        )
        # ======================================================
    # FAVORIS
    # ======================================================

    @staticmethod
    @transaction.atomic
    def add_favorite(Eleve, book):

        favorite, created = LibraryFavorite.objects.get_or_create(
            Eleve=Eleve,
            book=book,
        )

        if created:

            book.increment_favorites()

        return favorite

    @staticmethod
    @transaction.atomic
    def remove_favorite(Eleve, book):

        LibraryFavorite.objects.filter(
            Eleve=Eleve,
            book=book
        ).delete()

        if book.total_favorites > 0:

            book.total_favorites -= 1

            book.save(
                update_fields=["total_favorites"]
            )

    # ======================================================
    # NOTES
    # ======================================================

    @staticmethod
    @transaction.atomic
    def rate_book(Eleve, book, rating):

        obj, created = LibraryRating.objects.update_or_create(

            Eleve=Eleve,

            book=book,

            defaults={

                "rating": rating

            }

        )

        ratings = LibraryRating.objects.filter(
            book=book
        )

        average = ratings.aggregate(
            avg=Avg("rating")
        )["avg"] or 0

        book.average_rating = average

        book.total_ratings = ratings.count()

        book.save(
            update_fields=[
                "average_rating",
                "total_ratings"
            ]
        )

        return obj

    # ======================================================
    # AVIS
    # ======================================================

    @staticmethod
    def create_review(

        Eleve,

        book,

        title,

        review

    ):

        return LibraryReview.objects.create(

            Eleve=Eleve,

            book=book,

            title=title,

            review=review

        )

    # ======================================================
    # PROGRESSION
    # ======================================================

    @staticmethod
    @transaction.atomic
    def update_progress(

        Eleve,

        book,

        chapter,

        page,

        percentage,

        minutes

    ):

        progress, created = LibraryReadingProgress.objects.get_or_create(

            Eleve=Eleve,

            book=book,

            defaults={

                "current_page": page,

                "last_page": page,

                "current_chapter": chapter,

            }

        )

        progress.current_page = page

        progress.last_page = max(

            progress.last_page,

            page

        )

        progress.current_chapter = chapter

        progress.completion_percentage = percentage

        progress.minutes_read += minutes

        progress.sessions += 1

        progress.completed = percentage >= 100

        progress.save()

        return progress
        # ======================================================
    # CERTIFICATS
    # ======================================================

    @staticmethod
    @transaction.atomic
    def generate_certificate(Eleve, book):

        progress = LibraryReadingProgress.objects.filter(
            Eleve=Eleve,
            book=book
        ).first()

        if not progress:
            return None

        if progress.completion_percentage < 100:
            return None

        certificate_number = (
            f"LIB-"
            f"{Eleve.id}-"
            f"{book.id}-"
            f"{timezone.now().strftime('%Y%m%d%H%M%S')}"
        )

        certificate, created = LibraryCertificate.objects.get_or_create(
            Eleve=Eleve,
            book=book,
            defaults={
                "certificate_number": certificate_number,
                "score": progress.completion_percentage,
            }
        )

        return certificate

    # ======================================================
    # STATISTIQUES
    # ======================================================

    @staticmethod
    @transaction.atomic
    def update_statistics(book):

        statistics, created = LibraryStatistics.objects.get_or_create(
            book=book
        )

        statistics.total_Eleves = (
            LibraryReadingProgress.objects.filter(
                book=book
            ).count()
        )

        statistics.completed_Eleves = (
            LibraryReadingProgress.objects.filter(
                book=book,
                completed=True
            ).count()
        )

        statistics.average_progress = (
            LibraryReadingProgress.objects.filter(
                book=book
            ).aggregate(
                avg=Avg("completion_percentage")
            )["avg"] or 0
        )

        statistics.average_rating = (
            LibraryRating.objects.filter(
                book=book
            ).aggregate(
                avg=Avg("rating")
            )["avg"] or 0
        )

        statistics.save()

        return statistics

    # ======================================================
    # IA
    # ======================================================

    @staticmethod
    def recommend_books(Eleve):

        progress = LibraryReadingProgress.objects.filter(
            Eleve=Eleve,
            completed=True
        )

        subjects = []

        for item in progress:

            if item.book.subject:

                subjects.append(
                    item.book.subject.id
                )

        recommendations = LibraryBook.objects.filter(

            subject_id__in=subjects,

            is_published=True,

            active=True

        ).exclude(

            reading_progress__Eleve=Eleve

        ).distinct()[:20]

        return recommendations

    # ======================================================
    # POPULARITE
    # ======================================================

    @staticmethod
    def update_popularity(book):

        score = (

            book.total_views

            + (book.total_downloads * 5)

            + (book.total_reads * 3)

            + (book.total_favorites * 8)

            + (book.average_rating * 10)

        )

        return score

    # ======================================================
    # HISTORIQUE COMPLET
    # ======================================================

    @staticmethod
    def open_book(Eleve, book):

        book.increment_views()

        return LibraryHistory.objects.create(

            Eleve=Eleve,

            book=book,

            action="open",

            page=1

        )

    @staticmethod
    def finish_book(Eleve, book):

        return LibraryHistory.objects.create(

            Eleve=Eleve,

            book=book,

            action="finish",

            page=book.page_count

        )

    # ======================================================
    # REINITIALISATION
    # ======================================================

    @staticmethod
    def reset_progress(Eleve, book):

        LibraryReadingProgress.objects.filter(
            Eleve=Eleve,
            book=book
        ).delete()

        LibraryBookmark.objects.filter(
            Eleve=Eleve,
            book=book
        ).delete()

        return True