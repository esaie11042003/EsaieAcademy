import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify

# ==========================================================
#                  CORE DE LA PLATEFORME
# ==========================================================
#
# Cette application contient les fonctionnalités communes
# utilisées par toute la plateforme Esaïe Academy.
#
# Elle ne remplace aucune application.
#
# Toutes les autres applications (students, teachers,
# evaluations, results, configuration, documents...)
# utiliseront certains modèles de cette application.
#
# Cette application contiendra notamment :
#
# • Paramètres généraux de la plateforme
# • Paramètres globaux
# • Notifications
# • Historique des actions
# • Statistiques
# • Tableau de bord
# • Vérification des documents (plus tard)
# • QR Code (plus tard)
# • Signature numérique (plus tard)
#
# ==========================================================


# ==========================================================
#              PARAMÈTRES GLOBAUX
# ==========================================================
#
# Ce modèle permet de modifier le fonctionnement général
# de la plateforme sans modifier le code.
#
# Tous ces paramètres pourront être modifiés directement
# depuis l'administration Django.
#
# ==========================================================

class GlobalSetting(models.Model):

    # ------------------------------------------------------
    # Nom du paramètre
    # ------------------------------------------------------

    key = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Clé"
    )

    # ------------------------------------------------------
    # Valeur enregistrée
    # ------------------------------------------------------

    value = models.TextField(
        verbose_name="Valeur"
    )

    # ------------------------------------------------------
    # Description
    # ------------------------------------------------------

    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )

    # ------------------------------------------------------
    # Paramètre actif ?
    # ------------------------------------------------------

    active = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )

    # ------------------------------------------------------
    # Dates
    # ------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        verbose_name = "Paramètre global"

        verbose_name_plural = "Paramètres globaux"

        ordering = ["key"]

    def __str__(self):

        return self.key
    # ==========================================================
#              MODÈLE : JOURNAL DES ACTIVITÉS
# ==========================================================
#
# Ce modèle constitue le centre de traçabilité de toute
# la plateforme Esaïe Academy.
#
# Il enregistre toutes les actions importantes réalisées
# par les utilisateurs.
#
# Exemples :
#
# ✓ Connexion
# ✓ Déconnexion
# ✓ Création d'un élève
# ✓ Modification d'une note
# ✓ Impression d'un bulletin
# ✓ Paiement
# ✓ Téléchargement
# ✓ Suppression
#
# Plus tard, ce modèle permettra :
#
# • les audits
# • les statistiques
# • la sécurité
# • la détection des anomalies
# • l'historique complet de la plateforme
#
# ==========================================================

class ActivityLog(models.Model):

    # ======================================================
    # IDENTIFIANT UNIQUE
    # ======================================================
    #
    # UUID utilisé pour identifier chaque événement.
    #
    # Plus sécurisé qu'un simple identifiant numérique.
    #
    # ======================================================

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="UUID"
    )

    # ======================================================
    # UTILISATEUR
    # ======================================================

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activity_logs",
        verbose_name="Utilisateur"
    )

    # ======================================================
    # ETABLISSEMENT
    # ======================================================

    school = models.ForeignKey(
        "configuration.SchoolProfile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activity_logs",
        verbose_name="Établissement"
    )

    # ======================================================
    # ANNÉE SCOLAIRE
    # ======================================================

    school_year = models.ForeignKey(
        "school.SchoolYear",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activity_logs",
        verbose_name="Année scolaire"
    )

    # ======================================================
    # PÉRIODE
    # ======================================================

    period = models.ForeignKey(
        "school.Period",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activity_logs",
        verbose_name="Période"
    )

    # ======================================================
    # RÔLE DE L'UTILISATEUR
    # ======================================================
    #
    # Permet de savoir rapidement si l'action
    # provient d'un :
    #
    # - Élève
    # - Enseignant
    # - Personnel
    # - Administrateur
    #
    # ======================================================

    user_role = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Rôle"
    )

    # ======================================================
    # TYPE D'ACTION
    # ======================================================

    ACTION_CHOICES = (

        ("login", "Connexion"),

        ("logout", "Déconnexion"),

        ("create", "Création"),

        ("update", "Modification"),

        ("delete", "Suppression"),

        ("view", "Consultation"),

        ("download", "Téléchargement"),

        ("upload", "Téléversement"),

        ("print", "Impression"),

        ("payment", "Paiement"),

        ("validation", "Validation"),

        ("export", "Exportation"),

        ("import", "Importation"),

        ("other", "Autre"),
    )

    action = models.CharField(
        max_length=30,
        choices=ACTION_CHOICES,
        verbose_name="Action effectuée"
    )

    # ======================================================
    # NIVEAU DE CRITICITÉ
    # ======================================================

    CRITICALITY_CHOICES = (

        ("low", "Faible"),

        ("medium", "Moyenne"),

        ("high", "Élevée"),

        ("critical", "Critique"),
    )

    criticality = models.CharField(
        max_length=20,
        choices=CRITICALITY_CHOICES,
        default="low",
        verbose_name="Criticité"
    )
        # ======================================================
    #              APPLICATION CONCERNÉE
    # ======================================================
    #
    # Nom de l'application Django.
    #
    # Exemples :
    #
    # students
    # teachers
    # evaluations
    # results
    # payments
    # configuration
    #
    # ======================================================

    application = models.CharField(
        max_length=100,
        verbose_name="Application"
    )

    # ======================================================
    #              MODÈLE CONCERNÉ
    # ======================================================

    model_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Modèle"
    )

    # ======================================================
    #              IDENTIFIANT DE L'OBJET
    # ======================================================

    object_id = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        verbose_name="ID de l'objet"
    )

    # ======================================================
    #              DESCRIPTION DE L'ACTION
    # ======================================================

    description = models.TextField(
        verbose_name="Description"
    )

    # ======================================================
    #              ADRESSE IP
    # ======================================================

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="Adresse IP"
    )

    # ======================================================
    #              SESSION
    # ======================================================

    session_id = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Identifiant de session"
    )

    # ======================================================
    #              STATUT DE CONNEXION
    # ======================================================

    LOGIN_STATUS = (

        ("success", "Connexion réussie"),

        ("failed", "Connexion échouée"),

        ("logout", "Déconnexion"),

        ("expired", "Session expirée"),
    )

    login_status = models.CharField(
        max_length=20,
        choices=LOGIN_STATUS,
        blank=True,
        verbose_name="Statut de connexion"
    )

    # ======================================================
    #              TYPE D'APPAREIL
    # ======================================================
    #
    # Exemple :
    #
    # Ordinateur
    # Téléphone
    # Tablette
    #
    # ======================================================

    device_type = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Type d'appareil"
    )

    # ======================================================
    #              NOM DE L'APPAREIL
    # ======================================================

    device_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Nom de l'appareil"
    )

    # ======================================================
    #              SYSTÈME D'EXPLOITATION
    # ======================================================

    operating_system = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Système d'exploitation"
    )

    # ======================================================
    #              VERSION DU SYSTÈME
    # ======================================================

    operating_system_version = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Version du système"
    )

    # ======================================================
    #              NAVIGATEUR
    # ======================================================

    browser = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Navigateur"
    )

    # ======================================================
    #              VERSION DU NAVIGATEUR
    # ======================================================

    browser_version = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Version du navigateur"
    )

    # ======================================================
    #              LANGUE DU NAVIGATEUR
    # ======================================================

    browser_language = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Langue du navigateur"
    )

    # ======================================================
    #              RÉSOLUTION DE L'ÉCRAN
    # ======================================================

    screen_resolution = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Résolution d'écran"
    )

    # ======================================================
    #              FUSEAU HORAIRE
    # ======================================================

    timezone = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Fuseau horaire"
    )

    # ======================================================
    #              PAGE PRÉCÉDENTE
    # ======================================================

    referer = models.URLField(
        blank=True,
        verbose_name="Page précédente"
    )

    # ======================================================
    #              GÉOLOCALISATION
    # ======================================================

    country = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Pays"
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Ville"
    )

    # ======================================================
    #              DURÉE DE SESSION
    # ======================================================
    #
    # Durée en secondes.
    #
    # ======================================================

    session_duration = models.PositiveIntegerField(
        default=0,
        verbose_name="Durée de session (secondes)"
    )
        # ======================================================
    #              INFORMATIONS COMPLÉMENTAIRES
    # ======================================================
    #
    # Ce champ permet de stocker des informations
    # supplémentaires sans modifier le modèle.
    #
    # Exemples :
    #
    # {
    #     "ancienne_note": 12,
    #     "nouvelle_note": 15,
    #     "matiere": "Mathématiques"
    # }
    #
    # Ce champ rend le système très évolutif.
    #
    # ======================================================

    extra_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Informations complémentaires"
    )

    # ======================================================
    #              DATE DE CRÉATION
    # ======================================================

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de l'activité"
    )

    # ======================================================
    #              DATE DE MODIFICATION
    # ======================================================

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière modification"
    )

    # ======================================================
    #              ÉTAT DE L'ENREGISTREMENT
    # ======================================================

    active = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )

    # ======================================================
    #              CONFIGURATION DJANGO
    # ======================================================

    class Meta:

        verbose_name = "Journal d'activité"

        verbose_name_plural = "Journal des activités"

        ordering = [
            "-created_at",
        ]

        indexes = [

            models.Index(fields=["created_at"]),

            models.Index(fields=["action"]),

            models.Index(fields=["application"]),

            models.Index(fields=["criticality"]),

            models.Index(fields=["user"]),

            models.Index(fields=["school"]),

            models.Index(fields=["school_year"]),

            models.Index(fields=["period"]),
        ]

    # ======================================================
    #              REPRÉSENTATION
    # ======================================================

    def __str__(self):

        utilisateur = self.user if self.user else "Utilisateur inconnu"

        return (
            f"{utilisateur} | "
            f"{self.get_action_display()} | "
            f"{self.application}"
        )

    # ======================================================
    #              DESCRIPTION COMPLÈTE
    # ======================================================

    @property
    def full_description(self):
        """
        Retourne une description complète
        de l'activité.
        """

        utilisateur = self.user if self.user else "Système"

        return (
            f"{utilisateur} a effectué "
            f"l'action "
            f"'{self.get_action_display()}' "
            f"dans l'application "
            f"'{self.application}'."
        )
    # ==========================================================
#      DURÉE DE CONSERVATION DES JOURNAUX
# ==========================================================
#
# Permet à chaque établissement de choisir
# combien de temps conserver les journaux.
#
# Exemple :
#
# 1 an
# 3 ans
# 5 ans
# Illimité
#
# ==========================================================

RETENTION_CHOICES = (

    (365, "1 an"),

    (1095, "3 ans"),

    (1825, "5 ans"),

    (0, "Illimité"),
)
# ==========================================================
#                 MODÈLE : NOTIFICATION
# ==========================================================
#
# Ce modèle constitue le centre de communication de
# toute la plateforme Esaïe Academy.
#
# Toutes les applications pourront créer des
# notifications automatiquement.
#
# Exemples :
#
# ✓ Bulletin disponible
# ✓ Nouvelle note publiée
# ✓ Paiement validé
# ✓ Nouvelle épreuve disponible
# ✓ Nouveau devoir
# ✓ Nouveau message
# ✓ Convocation
# ✓ Information importante
#
# Plus tard, ces notifications pourront être envoyées :
#
# • Dans la plateforme
# • Par Email
# • Par SMS
# • Par WhatsApp
# • Par Notification Push
#
# ==========================================================

class Notification(models.Model):

    # ======================================================
    # IDENTIFIANT UNIQUE
    # ======================================================

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="UUID"
    )

    # ======================================================
    # ÉTABLISSEMENT
    # ======================================================

    school = models.ForeignKey(
        "configuration.SchoolProfile",
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
        blank=True,
        verbose_name="Établissement"
    )

    # ======================================================
    # EXPÉDITEUR
    # ======================================================
    #
    # Utilisateur ayant créé la notification.
    #
    # ======================================================

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sent_notifications",
        verbose_name="Expéditeur"
    )

    # ======================================================
    # DESTINATAIRE
    # ======================================================
    #
    # Notification destinée à un utilisateur.
    #
    # Les notifications de groupe seront ajoutées
    # dans la partie suivante.
    #
    # ======================================================

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="received_notifications",
        verbose_name="Destinataire"
    )

    # ======================================================
    # TYPE DE NOTIFICATION
    # ======================================================

    TYPE_CHOICES = (

        ("information", "Information"),

        ("success", "Succès"),

        ("warning", "Avertissement"),

        ("error", "Erreur"),

        ("urgent", "Urgente"),

        ("announcement", "Annonce"),
    )

    notification_type = models.CharField(
        max_length=30,
        choices=TYPE_CHOICES,
        default="information",
        verbose_name="Type"
    )

    # ======================================================
    # PRIORITÉ
    # ======================================================

    PRIORITY_CHOICES = (

        ("low", "Faible"),

        ("normal", "Normale"),

        ("high", "Élevée"),

        ("critical", "Critique"),
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="normal",
        verbose_name="Priorité"
    )

    # ======================================================
    # TITRE
    # ======================================================

    title = models.CharField(
        max_length=255,
        verbose_name="Titre"
    )

    # ======================================================
    # MESSAGE
    # ======================================================

    message = models.TextField(
        verbose_name="Message"
    )

    # ======================================================
    # DESCRIPTION COMPLÉMENTAIRE
    # ======================================================

    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
        # ======================================================
    #              DESTINATAIRES DE GROUPE
    # ======================================================
    #
    # Une notification peut être envoyée :
    #
    # - à plusieurs utilisateurs
    # - à une ou plusieurs classes
    # - à tous les élèves
    # - à tous les enseignants
    # - à tout le personnel
    # - à tout l'établissement
    #
    # ======================================================

    recipients = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="group_notifications",
        verbose_name="Destinataires multiples"
    )

    classes = models.ManyToManyField(
        "classes.Classe",
        blank=True,
        related_name="notifications",
        verbose_name="Classes concernées"
    )

    # ======================================================
    #              CIBLES DE LA NOTIFICATION
    # ======================================================

    send_to_students = models.BooleanField(
        default=False,
        verbose_name="Tous les élèves"
    )

    send_to_teachers = models.BooleanField(
        default=False,
        verbose_name="Tous les enseignants"
    )

    send_to_staff = models.BooleanField(
        default=False,
        verbose_name="Tout le personnel"
    )

    send_to_admins = models.BooleanField(
        default=False,
        verbose_name="Tous les administrateurs"
    )

    send_to_school = models.BooleanField(
        default=False,
        verbose_name="Tout l'établissement"
    )

    send_to_platform = models.BooleanField(
        default=False,
        verbose_name="Toute la plateforme"
    )

    # ======================================================
    #              CANAUX D'ENVOI
    # ======================================================
    #
    # Ces champs permettront plus tard d'envoyer
    # automatiquement les notifications par différents
    # moyens de communication.
    #
    # ======================================================

    send_in_app = models.BooleanField(
        default=True,
        verbose_name="Notification interne"
    )

    send_email = models.BooleanField(
        default=False,
        verbose_name="Envoyer par Email"
    )

    send_sms = models.BooleanField(
        default=False,
        verbose_name="Envoyer par SMS"
    )

    send_whatsapp = models.BooleanField(
        default=False,
        verbose_name="Envoyer par WhatsApp"
    )

    send_push = models.BooleanField(
        default=False,
        verbose_name="Notification Push"
    )

    # ======================================================
    #              PIÈCES JOINTES
    # ======================================================

    image = models.ImageField(
        upload_to="notifications/images/",
        blank=True,
        null=True,
        verbose_name="Image"
    )

    attachment = models.FileField(
        upload_to="notifications/files/",
        blank=True,
        null=True,
        verbose_name="Pièce jointe"
    )

    external_link = models.URLField(
        blank=True,
        verbose_name="Lien externe"
    )

    # ======================================================
    #              BOUTON D'ACTION
    # ======================================================
    #
    # Exemple :
    #
    # Télécharger le bulletin
    # Voir les notes
    # Régler le paiement
    #
    # ======================================================

    action_label = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Texte du bouton"
    )

    action_url = models.URLField(
        blank=True,
        verbose_name="Lien du bouton"
    )
        # ======================================================
    #              PROGRAMMATION
    # ======================================================
    #
    # Une notification peut être :
    #
    # • envoyée immédiatement
    # • programmée
    # • expirer automatiquement
    #
    # ======================================================

    scheduled_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date d'envoi programmée"
    )

    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date d'expiration"
    )

    # ======================================================
    #              ÉTAT DE LA NOTIFICATION
    # ======================================================

    STATUS_CHOICES = (

        ("draft", "Brouillon"),

        ("scheduled", "Programmée"),

        ("sent", "Envoyée"),

        ("read", "Lue"),

        ("archived", "Archivée"),

        ("expired", "Expirée"),

        ("cancelled", "Annulée"),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
        verbose_name="État"
    )

    # ======================================================
    #              LECTURE
    # ======================================================

    is_read = models.BooleanField(
        default=False,
        verbose_name="Notification lue"
    )

    read_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date de lecture"
    )

    # ======================================================
    #              STATISTIQUES
    # ======================================================
    #
    # Ces informations permettront de créer
    # des tableaux de bord très détaillés.
    #
    # ======================================================

    sent_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Nombre d'envois"
    )

    read_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Nombre de lectures"
    )

    failed_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Nombre d'échecs"
    )

    # ======================================================
    #              MÉTADONNÉES
    # ======================================================

    extra_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Informations complémentaires"
    )

    active = models.BooleanField(
        default=True,
        verbose_name="Active"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Créée le"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière modification"
    )

    # ======================================================
    #              CONFIGURATION DJANGO
    # ======================================================

    class Meta:

        verbose_name = "Notification"

        verbose_name_plural = "Notifications"

        ordering = [
            "-created_at",
        ]

        indexes = [

            models.Index(fields=["status"]),

            models.Index(fields=["notification_type"]),

            models.Index(fields=["priority"]),

            models.Index(fields=["created_at"]),

            models.Index(fields=["school"]),
        ]

    # ======================================================
    #              REPRÉSENTATION
    # ======================================================

    def __str__(self):

        return self.title

    # ======================================================
    #              NOTIFICATION EXPIRÉE ?
    # ======================================================

    @property
    def is_expired(self):

        from django.utils import timezone

        if self.expires_at:

            return timezone.now() > self.expires_at

        return False

    # ======================================================
    #              TAUX DE LECTURE
    # ======================================================

    @property
    def read_rate(self):

        if self.sent_count == 0:

            return 0

        return round(
            (self.read_count / self.sent_count) * 100,
            2
        )
    # ==========================================================
#          MODÈLE : STATISTIQUES DU TABLEAU DE BORD
# ==========================================================
#
# Ce modèle centralise les statistiques affichées
# sur le tableau de bord de la plateforme.
#
# Il permettra d'éviter de recalculer les données
# à chaque ouverture de la page d'accueil.
#
# Toutes les applications pourront mettre à jour
# automatiquement ces statistiques.
#
# ==========================================================

class DashboardStatistic(models.Model):

    # ======================================================
    # IDENTIFIANT UNIQUE
    # ======================================================

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="UUID"
    )

    # ======================================================
    # ÉTABLISSEMENT
    # ======================================================

    school = models.ForeignKey(
        "configuration.SchoolProfile",
        on_delete=models.CASCADE,
        related_name="dashboard_statistics",
        null=True,
        blank=True,
        verbose_name="Établissement"
    )

    # ======================================================
    # ANNÉE SCOLAIRE
    # ======================================================

    school_year = models.ForeignKey(
        "school.SchoolYear",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dashboard_statistics",
        verbose_name="Année scolaire"
    )

    # ======================================================
    # PÉRIODE
    # ======================================================

    period = models.ForeignKey(
        "school.Period",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dashboard_statistics",
        verbose_name="Période"
    )

    # ======================================================
    # DATE DE RÉFÉRENCE
    # ======================================================
    #
    # Exemple :
    #
    # 31/12/2026
    #
    # ======================================================

    statistic_date = models.DateField(
        verbose_name="Date des statistiques"
    )
        # ======================================================
    #              STATISTIQUES DES ÉLÈVES
    # ======================================================

    total_students = models.PositiveIntegerField(
        default=0,
        verbose_name="Nombre total d'élèves"
    )

    boys = models.PositiveIntegerField(
        default=0,
        verbose_name="Garçons"
    )

    girls = models.PositiveIntegerField(
        default=0,
        verbose_name="Filles"
    )

    new_students = models.PositiveIntegerField(
        default=0,
        verbose_name="Nouveaux élèves"
    )

    former_students = models.PositiveIntegerField(
        default=0,
        verbose_name="Anciens élèves"
    )

    # ======================================================
    #              STATISTIQUES DES ENSEIGNANTS
    # ======================================================

    total_teachers = models.PositiveIntegerField(
        default=0,
        verbose_name="Nombre d'enseignants"
    )

    active_teachers = models.PositiveIntegerField(
        default=0,
        verbose_name="Enseignants actifs"
    )

    unavailable_teachers = models.PositiveIntegerField(
        default=0,
        verbose_name="Enseignants indisponibles"
    )

    # ======================================================
    #              PERSONNEL
    # ======================================================

    total_staff = models.PositiveIntegerField(
        default=0,
        verbose_name="Personnel administratif"
    )

    # ======================================================
    #              CLASSES
    # ======================================================

    total_classes = models.PositiveIntegerField(
        default=0,
        verbose_name="Nombre de classes"
    )

    active_classes = models.PositiveIntegerField(
        default=0,
        verbose_name="Classes actives"
    )

    # ======================================================
    #              MATIÈRES
    # ======================================================

    total_subjects = models.PositiveIntegerField(
        default=0,
        verbose_name="Nombre de matières"
    )

    # ======================================================
    #              ÉVALUATIONS
    # ======================================================

    total_evaluations = models.PositiveIntegerField(
        default=0,
        verbose_name="Évaluations"
    )

    completed_evaluations = models.PositiveIntegerField(
        default=0,
        verbose_name="Évaluations terminées"
    )

    # ======================================================
    #              BULLETINS
    # ======================================================

    generated_reports = models.PositiveIntegerField(
        default=0,
        verbose_name="Bulletins générés"
    )

    printed_reports = models.PositiveIntegerField(
        default=0,
        verbose_name="Bulletins imprimés"
    )

    downloaded_reports = models.PositiveIntegerField(
        default=0,
        verbose_name="Bulletins téléchargés"
    )

    # ======================================================
    #              DOCUMENTS
    # ======================================================

    uploaded_documents = models.PositiveIntegerField(
        default=0,
        verbose_name="Documents publiés"
    )

    downloaded_documents = models.PositiveIntegerField(
        default=0,
        verbose_name="Documents téléchargés"
    )

    # ======================================================
    #              UTILISATEURS
    # ======================================================

    total_users = models.PositiveIntegerField(
        default=0,
        verbose_name="Nombre d'utilisateurs"
    )

    online_users = models.PositiveIntegerField(
        default=0,
        verbose_name="Utilisateurs en ligne"
    )

    active_sessions = models.PositiveIntegerField(
        default=0,
        verbose_name="Sessions actives"
    )
        # ======================================================
    #          TYPE DE STATISTIQUES
    # ======================================================
    #
    # Ce champ indique la période concernée par
    # les statistiques enregistrées.
    #
    # Il permettra d'utiliser le même modèle pour
    # produire des tableaux de bord journaliers,
    # mensuels, trimestriels, annuels ou globaux.
    #
    # Exemples :
    #
    # - Nombre d'élèves aujourd'hui
    # - Paiements du mois
    # - Résultats du 2ème trimestre
    # - Statistiques de l'année scolaire
    # - Statistiques générales de l'établissement
    #
    # ======================================================

    STATISTIC_TYPE_CHOICES = (

        ("daily", "Quotidiennes"),

        ("weekly", "Hebdomadaires"),

        ("monthly", "Mensuelles"),

        ("trimester", "Trimestrielles"),

        ("semester", "Semestrielles"),

        ("yearly", "Annuelles"),

        ("global", "Générales"),
    )

    statistic_type = models.CharField(
        max_length=20,
        choices=STATISTIC_TYPE_CHOICES,
        default="global",
        verbose_name="Type de statistiques"
    )

    # ======================================================
    #          STATISTIQUES PÉDAGOGIQUES
    # ======================================================

    average_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name="Moyenne générale"
    )

    highest_average = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name="Meilleure moyenne"
    )

    lowest_average = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name="Plus faible moyenne"
    )

    success_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name="Taux de réussite (%)"
    )

    failure_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name="Taux d'échec (%)"
    )

    attendance_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name="Taux de présence (%)"
    )

    absence_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name="Taux d'absence (%)"
    )

    admitted_students = models.PositiveIntegerField(
        default=0,
        verbose_name="Élèves admis"
    )

    repeating_students = models.PositiveIntegerField(
        default=0,
        verbose_name="Élèves redoublants"
    )

    transferred_students = models.PositiveIntegerField(
        default=0,
        verbose_name="Élèves transférés"
    )

    excluded_students = models.PositiveIntegerField(
        default=0,
        verbose_name="Élèves exclus"
    )
        # ======================================================
    #              STATISTIQUES FINANCIÈRES
    # ======================================================
    #
    # Ces informations permettront au chef
    # d'établissement de suivre la situation
    # financière de son école.
    #
    # ======================================================

    total_expected_fees = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="Montant total attendu"
    )

    total_paid_fees = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="Montant total encaissé"
    )

    total_remaining_fees = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="Montant restant"
    )

    successful_payments = models.PositiveIntegerField(
        default=0,
        verbose_name="Paiements réussis"
    )

    pending_payments = models.PositiveIntegerField(
        default=0,
        verbose_name="Paiements en attente"
    )

    failed_payments = models.PositiveIntegerField(
        default=0,
        verbose_name="Paiements échoués"
    )

    scholarship_students = models.PositiveIntegerField(
        default=0,
        verbose_name="Élèves boursiers"
    )

    discounted_students = models.PositiveIntegerField(
        default=0,
        verbose_name="Élèves bénéficiant d'une réduction"
    )

    # ======================================================
    #              STATISTIQUES DE LA PLATEFORME
    # ======================================================

    total_connections = models.PositiveIntegerField(
        default=0,
        verbose_name="Nombre de connexions"
    )

    unique_visitors = models.PositiveIntegerField(
        default=0,
        verbose_name="Visiteurs uniques"
    )

    generated_notifications = models.PositiveIntegerField(
        default=0,
        verbose_name="Notifications envoyées"
    )

    downloaded_files = models.PositiveIntegerField(
        default=0,
        verbose_name="Téléchargements"
    )

    generated_reports_total = models.PositiveIntegerField(
        default=0,
        verbose_name="Rapports générés"
    )

    recorded_activities = models.PositiveIntegerField(
        default=0,
        verbose_name="Activités enregistrées"
    )

    # ======================================================
    #              INFORMATIONS COMPLÉMENTAIRES
    # ======================================================

    extra_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Informations complémentaires"
    )

    # ======================================================
    #              ÉTAT
    # ======================================================

    active = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )

    # ======================================================
    #              HORODATAGE
    # ======================================================

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Créé le"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière modification"
    )

    # ======================================================
    #              CONFIGURATION DJANGO
    # ======================================================

    class Meta:

        verbose_name = "Statistique"

        verbose_name_plural = "Statistiques"

        ordering = [
            "-statistic_date",
            "-created_at",
        ]

        indexes = [

            models.Index(fields=["school"]),

            models.Index(fields=["school_year"]),

            models.Index(fields=["period"]),

            models.Index(fields=["statistic_type"]),

            models.Index(fields=["statistic_date"]),
        ]

    # ======================================================
    #              REPRÉSENTATION
    # ======================================================

    def __str__(self):

        return (
            f"{self.school} - "
            f"{self.get_statistic_type_display()} - "
            f"{self.statistic_date}"
        )
    # ==========================================================
#            MODÈLE : PARAMÈTRES DE LA PLATEFORME
# ==========================================================
#
# Ce modèle centralise tous les paramètres généraux
# de fonctionnement de la plateforme.
#
# Grâce à lui, l'administrateur pourra activer ou
# désactiver certaines fonctionnalités directement
# depuis l'administration Django.
#
# Une seule configuration sera utilisée par toute
# la plateforme.
#
# ==========================================================

class PlatformSettings(models.Model):

    # ======================================================
    # IDENTIFIANT UNIQUE
    # ======================================================

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="UUID"
    )

    # ======================================================
    # NOM DE LA PLATEFORME
    # ======================================================

    platform_name = models.CharField(
        max_length=200,
        default="Esaïe Academy",
        verbose_name="Nom de la plateforme"
    )

    # ======================================================
    # VERSION
    # ======================================================

    platform_version = models.CharField(
        max_length=30,
        default="1.0.0",
        verbose_name="Version"
    )

    # ======================================================
    # DESCRIPTION
    # ======================================================

    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )

    # ======================================================
    # LOGO DE LA PLATEFORME
    # ======================================================

    logo = models.ImageField(
        upload_to="platform/logo/",
        blank=True,
        null=True,
        verbose_name="Logo"
    )

    # ======================================================
    # FAVICON
    # ======================================================

    favicon = models.ImageField(
        upload_to="platform/favicon/",
        blank=True,
        null=True,
        verbose_name="Favicon"
    )

    # ======================================================
    # MODE MAINTENANCE
    # ======================================================

    maintenance_mode = models.BooleanField(
        default=False,
        verbose_name="Mode maintenance"
    )

    maintenance_message = models.TextField(
        blank=True,
        verbose_name="Message de maintenance"
    )

    # ======================================================
    # MODE DÉMONSTRATION
    # ======================================================

    demo_mode = models.BooleanField(
        default=False,
        verbose_name="Mode démonstration"
    )
        # ======================================================
    #      GESTION DES ÉTABLISSEMENTS
    # ======================================================
    #
    # Ces paramètres permettent de contrôler
    # la création et la gestion des établissements.
    #
    # ======================================================

    allow_school_registration = models.BooleanField(
        default=True,
        verbose_name="Autoriser la création d'établissements"
    )

    require_school_validation = models.BooleanField(
        default=True,
        verbose_name="Validation des établissements obligatoire"
    )

    max_schools = models.PositiveIntegerField(
        default=0,
        verbose_name="Nombre maximal d'établissements (0 = illimité)"
    )

    # ======================================================
    #      GESTION DES UTILISATEURS
    # ======================================================

    allow_user_registration = models.BooleanField(
        default=False,
        verbose_name="Autoriser l'inscription des utilisateurs"
    )

    require_email_verification = models.BooleanField(
        default=False,
        verbose_name="Vérification de l'adresse email"
    )

    require_phone_verification = models.BooleanField(
        default=False,
        verbose_name="Vérification du numéro de téléphone"
    )

    enable_two_factor_authentication = models.BooleanField(
        default=False,
        verbose_name="Authentification à deux facteurs (2FA)"
    )

    minimum_password_length = models.PositiveIntegerField(
        default=8,
        verbose_name="Longueur minimale du mot de passe"
    )

    # ======================================================
    #      GESTION SCOLAIRE
    # ======================================================

    enable_school_years = models.BooleanField(
        default=True,
        verbose_name="Activer les années scolaires"
    )

    enable_periods = models.BooleanField(
        default=True,
        verbose_name="Activer les périodes"
    )

    enable_subjects = models.BooleanField(
        default=True,
        verbose_name="Activer les matières"
    )

    enable_evaluations = models.BooleanField(
        default=True,
        verbose_name="Activer les évaluations"
    )

    enable_results = models.BooleanField(
        default=True,
        verbose_name="Activer les résultats"
    )

    enable_report_cards = models.BooleanField(
        default=True,
        verbose_name="Activer les bulletins"
    )

    enable_rankings = models.BooleanField(
        default=True,
        verbose_name="Activer les classements"
    )

    enable_statistics = models.BooleanField(
        default=True,
        verbose_name="Activer les statistiques"
    )
        # ======================================================
    #      GESTION DES MODULES
    # ======================================================
    #
    # Chaque établissement pourra activer ou
    # désactiver les différents modules de la
    # plateforme selon ses besoins.
    #
    # Aucun développement supplémentaire ne sera
    # nécessaire : il suffira de cocher ou décocher
    # les modules dans l'administration.
    #
    # ======================================================

    enable_student_management = models.BooleanField(
        default=True,
        verbose_name="Gestion des élèves"
    )

    enable_teacher_management = models.BooleanField(
        default=True,
        verbose_name="Gestion des enseignants"
    )

    enable_staff_management = models.BooleanField(
        default=True,
        verbose_name="Gestion du personnel"
    )

    enable_class_management = models.BooleanField(
        default=True,
        verbose_name="Gestion des classes"
    )

    enable_subject_management = models.BooleanField(
        default=True,
        verbose_name="Gestion des matières"
    )

    enable_library = models.BooleanField(
        default=False,
        verbose_name="Bibliothèque"
    )

    enable_competitions = models.BooleanField(
        default=True,
        verbose_name="Concours"
    )

    enable_document_center = models.BooleanField(
        default=True,
        verbose_name="Centre de documents"
    )

    enable_assignments = models.BooleanField(
        default=True,
        verbose_name="Devoirs"
    )

    enable_attendance = models.BooleanField(
        default=True,
        verbose_name="Gestion des présences"
    )

    enable_timetable = models.BooleanField(
        default=True,
        verbose_name="Emploi du temps"
    )

    enable_discipline = models.BooleanField(
        default=False,
        verbose_name="Discipline"
    )

    enable_health = models.BooleanField(
        default=False,
        verbose_name="Santé scolaire"
    )

    enable_boarding = models.BooleanField(
        default=False,
        verbose_name="Internat"
    )

    enable_transport = models.BooleanField(
        default=False,
        verbose_name="Transport scolaire"
    )

    enable_canteen = models.BooleanField(
        default=False,
        verbose_name="Cantine scolaire"
    )

    enable_payments = models.BooleanField(
        default=True,
        verbose_name="Paiements"
    )

    enable_accounting = models.BooleanField(
        default=False,
        verbose_name="Comptabilité"
    )

    enable_notifications = models.BooleanField(
        default=True,
        verbose_name="Notifications"
    )

    enable_internal_messages = models.BooleanField(
        default=True,
        verbose_name="Messagerie interne"
    )

    enable_forum = models.BooleanField(
        default=True,
        verbose_name="Forum"
    )

    enable_statistics_dashboard = models.BooleanField(
        default=True,
        verbose_name="Tableau de bord"
    )
        # ======================================================
    #      FONCTIONNALITÉS AVANCÉES
    # ======================================================
    #
    # Ces paramètres permettent d'activer ou
    # désactiver les principales fonctionnalités
    # transversales de la plateforme.
    #
    # Les fonctionnalités plus spécifiques
    # pourront être gérées ultérieurement par
    # un modèle FeatureFlag.
    #
    # ======================================================

    enable_pdf_export = models.BooleanField(
        default=True,
        verbose_name="Export PDF"
    )

    enable_excel_export = models.BooleanField(
        default=True,
        verbose_name="Export Excel"
    )

    enable_qr_code = models.BooleanField(
        default=True,
        verbose_name="QR Code"
    )

    enable_barcode = models.BooleanField(
        default=False,
        verbose_name="Code-barres"
    )

    enable_electronic_signature = models.BooleanField(
        default=False,
        verbose_name="Signature électronique"
    )

    enable_auto_backup = models.BooleanField(
        default=True,
        verbose_name="Sauvegarde automatique"
    )

    enable_activity_logs = models.BooleanField(
        default=True,
        verbose_name="Journal des activités"
    )

    enable_api = models.BooleanField(
        default=False,
        verbose_name="API"
    )

    enable_dark_mode = models.BooleanField(
        default=True,
        verbose_name="Mode sombre"
    )

    enable_multilingual = models.BooleanField(
        default=True,
        verbose_name="Mode multilingue"
    )

    enable_email_notifications = models.BooleanField(
        default=True,
        verbose_name="Notifications par email"
    )

    enable_sms_notifications = models.BooleanField(
        default=False,
        verbose_name="Notifications par SMS"
    )

    enable_whatsapp_notifications = models.BooleanField(
        default=False,
        verbose_name="Notifications WhatsApp"
    )

    enable_push_notifications = models.BooleanField(
        default=False,
        verbose_name="Notifications Push"
    )

    enable_public_registration = models.BooleanField(
        default=False,
        verbose_name="Inscription publique"
    )

    enable_online_payments = models.BooleanField(
        default=True,
        verbose_name="Paiements en ligne"
    )

    enable_download_center = models.BooleanField(
        default=True,
        verbose_name="Téléchargement des documents"
    )

    enable_online_results = models.BooleanField(
        default=True,
        verbose_name="Consultation des résultats en ligne"
    )

    enable_online_report_cards = models.BooleanField(
        default=True,
        verbose_name="Consultation des bulletins en ligne"
    )
        # ======================================================
    #      PARAMÈTRES RÉGIONAUX
    # ======================================================
    #
    # Ces paramètres définissent les préférences
    # générales de la plateforme.
    #
    # ======================================================

    default_language = models.CharField(
        max_length=20,
        default="fr",
        verbose_name="Langue par défaut"
    )

    default_timezone = models.CharField(
        max_length=100,
        default="Africa/Porto-Novo",
        verbose_name="Fuseau horaire"
    )

    default_currency = models.CharField(
        max_length=10,
        default="XOF",
        verbose_name="Devise"
    )

    date_format = models.CharField(
        max_length=30,
        default="d/m/Y",
        verbose_name="Format de date"
    )

    # ======================================================
    #      LICENCE DE LA PLATEFORME
    # ======================================================

    LICENSE_CHOICES = (

        ("free", "Gratuit"),

        ("basic", "Basic"),

        ("standard", "Standard"),

        ("premium", "Premium"),

        ("enterprise", "Entreprise"),

        ("ministry", "Ministère"),
    )

    license_type = models.CharField(
        max_length=20,
        choices=LICENSE_CHOICES,
        default="free",
        verbose_name="Type de licence"
    )

    license_start = models.DateField(
        null=True,
        blank=True,
        verbose_name="Début de licence"
    )

    license_end = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fin de licence"
    )

    # ======================================================
    #      INFORMATIONS COMPLÉMENTAIRES
    # ======================================================

    extra_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Informations complémentaires"
    )

    # ======================================================
    #      ÉTAT
    # ======================================================

    active = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )

    # ======================================================
    #      HORODATAGE
    # ======================================================

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Créé le"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière modification"
    )

    # ======================================================
    #      CONFIGURATION DJANGO
    # ======================================================

    class Meta:

        verbose_name = "Paramètre de la plateforme"

        verbose_name_plural = "Paramètres de la plateforme"

    # ======================================================
    #      REPRÉSENTATION
    # ======================================================

    def __str__(self):

        return self.platform_name
    # ==========================================================
#             MODÈLE : FEATURE FLAG
# ==========================================================
#
# Ce modèle permet d'activer ou de désactiver
# dynamiquement une fonctionnalité de la plateforme.
#
# Contrairement à PlatformSettings qui contient
# les paramètres globaux et stables,
# FeatureFlag permet d'ajouter de nouvelles
# fonctionnalités sans modifier la structure
# du modèle PlatformSettings.
#
# Exemples :
#
# - QR Code sécurisé
# - Signature électronique
# - IA de correction
# - API REST
# - Paiement Mobile Money
# - Paiement Carte Bancaire
# - WhatsApp
# - SMS
#
# ==========================================================

class FeatureFlag(models.Model):

    # ======================================================
    # IDENTIFIANT UNIQUE
    # ======================================================

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="UUID"
    )

    # ======================================================
    # NOM DE LA FONCTIONNALITÉ
    # ======================================================

    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Nom"
    )

    # ======================================================
    # CODE UNIQUE
    # ======================================================
    #
    # Exemple :
    #
    # qr_code
    # electronic_signature
    # mobile_money
    #
    # ======================================================

    code = models.SlugField(
        unique=True,
        verbose_name="Code"
    )

    # ======================================================
    # DESCRIPTION
    # ======================================================

    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )

    # ======================================================
    # CATÉGORIE
    # ======================================================

    CATEGORY_CHOICES = (

        ("security", "Sécurité"),

        ("payment", "Paiement"),

        ("education", "Pédagogie"),

        ("communication", "Communication"),

        ("reports", "Bulletins"),

        ("integration", "Intégration"),

        ("ai", "Intelligence Artificielle"),

        ("system", "Système"),

        ("other", "Autre"),
    )

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default="other",
        verbose_name="Catégorie"
    )

    # ======================================================
    # ÉTAT
    # ======================================================

    enabled = models.BooleanField(
        default=False,
        verbose_name="Fonction activée"
    )
        # ======================================================
    #      DISPONIBILITÉ DE LA FONCTIONNALITÉ
    # ======================================================
    #
    # Ces champs permettent de définir où
    # la fonctionnalité est disponible.
    #
    # ======================================================

    available_for_platform = models.BooleanField(
        default=True,
        verbose_name="Disponible sur toute la plateforme"
    )

    available_for_school = models.BooleanField(
        default=True,
        verbose_name="Disponible pour les établissements"
    )

    school = models.ForeignKey(
        "configuration.SchoolProfile",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="feature_flags",
        verbose_name="Établissement concerné"
    )

    # ======================================================
    #      LICENCE MINIMALE REQUISE
    # ======================================================
    #
    # Permet de réserver certaines fonctionnalités
    # à certaines formules d'abonnement.
    #
    # ======================================================

    LICENSE_CHOICES = (

        ("free", "Gratuit"),

        ("basic", "Basic"),

        ("standard", "Standard"),

        ("premium", "Premium"),

        ("enterprise", "Entreprise"),

        ("ministry", "Ministère"),
    )

    minimum_license = models.CharField(
        max_length=20,
        choices=LICENSE_CHOICES,
        default="free",
        verbose_name="Licence minimale"
    )

    # ======================================================
    #      DATE D'ACTIVATION
    # ======================================================

    starts_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Début d'activation"
    )

    # ======================================================
    #      DATE D'EXPIRATION
    # ======================================================

    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fin d'activation"
    )

    # ======================================================
    #      BÊTA
    # ======================================================
    #
    # Une fonctionnalité peut être en phase
    # de test avant d'être rendue publique.
    #
    # ======================================================

    is_beta = models.BooleanField(
        default=False,
        verbose_name="Fonctionnalité en bêta"
    )

    # ======================================================
    #      EXPÉRIMENTALE
    # ======================================================

    is_experimental = models.BooleanField(
        default=False,
        verbose_name="Fonctionnalité expérimentale"
    )
        # ======================================================
    #      AUTORISATIONS
    # ======================================================
    #
    # Certaines fonctionnalités peuvent être
    # réservées à certains rôles ou permissions.
    #
    # Exemples :
    #
    # - Directeur
    # - Censeur
    # - Comptable
    # - Administrateur
    #
    # ======================================================

    required_role = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Rôle requis"
    )

    required_permission = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Permission requise"
    )

    required_group = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Groupe requis"
    )

    # ======================================================
    #      VERSION MINIMALE
    # ======================================================
    #
    # Permet de rendre une fonctionnalité
    # disponible uniquement à partir d'une
    # certaine version de la plateforme.
    #
    # Exemple :
    #
    # 2.0.0
    # 3.5.1
    #
    # ======================================================

    minimum_platform_version = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Version minimale"
    )

    # ======================================================
    #      ORDRE D'AFFICHAGE
    # ======================================================

    display_order = models.PositiveIntegerField(
        default=1,
        verbose_name="Ordre d'affichage"
    )

    # ======================================================
    #      INFORMATIONS COMPLÉMENTAIRES
    # ======================================================

    extra_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Informations complémentaires"
    )

    # ======================================================
    #      HORODATAGE
    # ======================================================

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Créée le"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière modification"
    )

    # ======================================================
    #      CONFIGURATION DJANGO
    # ======================================================

    class Meta:

        verbose_name = "Fonctionnalité"

        verbose_name_plural = "Fonctionnalités"

        ordering = [
            "category",
            "display_order",
            "name",
        ]

        indexes = [

            models.Index(fields=["code"]),

            models.Index(fields=["category"]),

            models.Index(fields=["enabled"]),

            models.Index(fields=["minimum_license"]),
        ]

    # ======================================================
    #      REPRÉSENTATION
    # ======================================================

    def __str__(self):

        return self.name

    # ======================================================
    #      FONCTIONNALITÉ ACTIVE ?
    # ======================================================

    @property
    def is_active(self):

        from django.utils import timezone

        now = timezone.now()

        if not self.enabled:
            return False

        if self.starts_at and now < self.starts_at:
            return False

        if self.expires_at and now > self.expires_at:
            return False

        return True

# ==========================================================
#            MODÈLE : ANNONCES SYSTÈME
# ==========================================================
#
# Ce modèle permet de diffuser des annonces
# officielles dans toute la plateforme.
#
# Exemples :
#
# - Rentrée scolaire
# - Maintenance
# - Résultats disponibles
# - Bulletins disponibles
# - Nouveau concours
# - Information importante
# - Message du directeur
# - Message du ministère
#
# Les annonces pourront apparaître :
#
# ✓ Page d'accueil
# ✓ Tableau de bord
# ✓ Application mobile
# ✓ Notifications
# ✓ Email
#
# ==========================================================

class SystemAnnouncement(models.Model):

    # ======================================================
    # IDENTIFIANT UNIQUE
    # ======================================================

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="UUID"
    )

    # ======================================================
    # ÉTABLISSEMENT
    # ======================================================

    school = models.ForeignKey(
        "configuration.SchoolProfile",
        on_delete=models.CASCADE,
        related_name="announcements",
        null=True,
        blank=True,
        verbose_name="Établissement"
    )

    # ======================================================
    # CRÉATEUR
    # ======================================================

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_announcements",
        verbose_name="Créé par"
    )

    # ======================================================
    # TITRE
    # ======================================================

    title = models.CharField(
        max_length=255,
        verbose_name="Titre"
    )

    # ======================================================
    # CONTENU
    # ======================================================

    message = models.TextField(
        verbose_name="Message"
    )

    # ======================================================
    # DESCRIPTION
    # ======================================================

    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )

    # ======================================================
    # TYPE D'ANNONCE
    # ======================================================

    ANNOUNCEMENT_TYPE_CHOICES = (

        ("information", "Information"),

        ("success", "Succès"),

        ("warning", "Avertissement"),

        ("danger", "Urgente"),

        ("maintenance", "Maintenance"),

        ("event", "Événement"),

        ("education", "Pédagogique"),

        ("competition", "Concours"),

        ("result", "Résultats"),

        ("report", "Bulletins"),
    )

    announcement_type = models.CharField(
        max_length=30,
        choices=ANNOUNCEMENT_TYPE_CHOICES,
        default="information",
        verbose_name="Type d'annonce"
    )

    # ======================================================
    # PRIORITÉ
    # ======================================================

    PRIORITY_CHOICES = (

        ("low", "Faible"),

        ("normal", "Normale"),

        ("high", "Élevée"),

        ("critical", "Critique"),
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="normal",
        verbose_name="Priorité"
    )
        # ======================================================
    #      IMAGE DE L'ANNONCE
    # ======================================================

    image = models.ImageField(
        upload_to="announcements/images/",
        blank=True,
        null=True,
        verbose_name="Image"
    )

    # ======================================================
    #      PIÈCE JOINTE
    # ======================================================
    #
    # Exemple :
    #
    # - PDF
    # - Document Word
    # - Circulaire
    # - Règlement intérieur
    #
    # ======================================================

    attachment = models.FileField(
        upload_to="announcements/files/",
        blank=True,
        null=True,
        verbose_name="Pièce jointe"
    )

    # ======================================================
    #      LIEN EXTERNE
    # ======================================================

    external_url = models.URLField(
        blank=True,
        verbose_name="Lien externe"
    )

    # ======================================================
    #      BOUTON D'ACTION
    # ======================================================
    #
    # Exemples :
    #
    # Télécharger
    # Voir les résultats
    # Voir les bulletins
    # Participer
    #
    # ======================================================

    action_label = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Texte du bouton"
    )

    action_url = models.URLField(
        blank=True,
        verbose_name="Lien du bouton"
    )

    # ======================================================
    #      PÉRIODE D'AFFICHAGE
    # ======================================================

    starts_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Début de publication"
    )

    ends_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fin de publication"
    )

    # ======================================================
    #      CANAUX DE DIFFUSION
    # ======================================================
    #
    # Une annonce peut être affichée sur
    # plusieurs supports simultanément.
    #
    # ======================================================

    show_on_homepage = models.BooleanField(
        default=True,
        verbose_name="Afficher sur la page d'accueil"
    )

    show_on_dashboard = models.BooleanField(
        default=True,
        verbose_name="Afficher sur le tableau de bord"
    )

    show_as_notification = models.BooleanField(
        default=False,
        verbose_name="Créer une notification"
    )

    send_by_email = models.BooleanField(
        default=False,
        verbose_name="Envoyer par email"
    )

    send_by_sms = models.BooleanField(
        default=False,
        verbose_name="Envoyer par SMS"
    )

    send_by_whatsapp = models.BooleanField(
        default=False,
        verbose_name="Envoyer par WhatsApp"
    )

    send_as_push = models.BooleanField(
        default=False,
        verbose_name="Notification Push"
    )

    # ======================================================
    #      CIBLE DE L'ANNONCE
    # ======================================================

    is_global = models.BooleanField(
        default=False,
        verbose_name="Annonce globale"
    )

    visible_to_students = models.BooleanField(
        default=True,
        verbose_name="Visible par les élèves"
    )

    visible_to_teachers = models.BooleanField(
        default=True,
        verbose_name="Visible par les enseignants"
    )

    visible_to_staff = models.BooleanField(
        default=True,
        verbose_name="Visible par le personnel"
    )

    visible_to_parents = models.BooleanField(
        default=True,
        verbose_name="Visible par les parents"
    )
        # ======================================================
    #      ANNONCE ÉPINGLÉE
    # ======================================================
    #
    # Une annonce épinglée restera toujours
    # affichée en haut des pages concernées.
    #
    # Exemple :
    #
    # - Rentrée scolaire
    # - Maintenance importante
    # - Message du Directeur
    #
    # ======================================================

    is_pinned = models.BooleanField(
        default=False,
        verbose_name="Annonce épinglée"
    )

    # ======================================================
    #      BANDEAU D'INFORMATION
    # ======================================================
    #
    # Permet d'afficher l'annonce sous forme
    # de bandeau défilant sur la plateforme.
    #
    # ======================================================

    show_as_banner = models.BooleanField(
        default=False,
        verbose_name="Afficher comme bandeau"
    )

    # ======================================================
    #      ÉTAT DE L'ANNONCE
    # ======================================================

    STATUS_CHOICES = (

        ("draft", "Brouillon"),

        ("scheduled", "Programmée"),

        ("published", "Publiée"),

        ("archived", "Archivée"),

        ("expired", "Expirée"),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
        verbose_name="État"
    )

    # ======================================================
    #      STATISTIQUES
    # ======================================================

    views = models.PositiveIntegerField(
        default=0,
        verbose_name="Nombre de vues"
    )

    clicks = models.PositiveIntegerField(
        default=0,
        verbose_name="Nombre de clics"
    )

    email_sent = models.PositiveIntegerField(
        default=0,
        verbose_name="Emails envoyés"
    )

    sms_sent = models.PositiveIntegerField(
        default=0,
        verbose_name="SMS envoyés"
    )

    whatsapp_sent = models.PositiveIntegerField(
        default=0,
        verbose_name="Messages WhatsApp envoyés"
    )

    push_sent = models.PositiveIntegerField(
        default=0,
        verbose_name="Notifications Push envoyées"
    )

    # ======================================================
    #      OPTIONS
    # ======================================================

    require_acknowledgement = models.BooleanField(
        default=False,
        verbose_name="Accusé de lecture obligatoire"
    )

    active = models.BooleanField(
        default=True,
        verbose_name="Active"
    )

    # ======================================================
    #      INFORMATIONS COMPLÉMENTAIRES
    # ======================================================

    extra_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Informations complémentaires"
    )

    # ======================================================
    #      HORODATAGE
    # ======================================================

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Créée le"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière modification"
    )

    # ======================================================
    #      CONFIGURATION DJANGO
    # ======================================================

    class Meta:

        verbose_name = "Annonce"

        verbose_name_plural = "Annonces"

        ordering = [
            "-is_pinned",
            "-priority",
            "-starts_at",
            "-created_at",
        ]

        indexes = [

            models.Index(fields=["status"]),

            models.Index(fields=["announcement_type"]),

            models.Index(fields=["priority"]),

            models.Index(fields=["starts_at"]),

            models.Index(fields=["school"]),
        ]

    # ======================================================
    #      REPRÉSENTATION
    # ======================================================

    def __str__(self):

        return self.title

    # ======================================================
    #      ANNONCE ACTIVE ?
    # ======================================================

    @property
    def is_active(self):

        from django.utils import timezone

        now = timezone.now()

        if not self.active:
            return False

        if self.status != "published":
            return False

        if self.starts_at and now < self.starts_at:
            return False

        if self.ends_at and now > self.ends_at:
            return False

        return True

    # ======================================================
    #      TAUX DE CLIC
    # ======================================================

    @property
    def click_rate(self):

        if self.views == 0:
            return 0

        return round(
            (self.clicks / self.views) * 100,
            2
        )