"""
Logique de calcul des résultats scolaires.

Règles retenues (validées avec l'utilisateur) :
- Moyenne d'une matière = (moyenne des interrogations + devoir_1 + devoir_2) / 3
- Les notes sont toujours sur 20 (pas de normalisation via note_sur)
- Décision automatique : moyenne_generale >= 10 => Admis, sinon Redouble
- Une note "absente" (Note.absent = True) compte pour 0
- Une note supprimée (is_deleted = True) est ignorée
- Le classement (rang) utilise le rang "à égalité" : deux élèves avec la
  même moyenne partagent le même rang, et le rang suivant saute le nombre
  d'ex-aequo (ex: 1, 2, 2, 4).
"""

from decimal import Decimal

from django.db import transaction

from assignments.models import Assignment
from students.models import Eleve
from evaluations.models import Note
from .models import SubjectResult, StudentResult


# ============================================================
# SEUILS DE MENTION
# ============================================================
# Ajuste librement ces seuils selon les usages de ton école.

SEUILS_MENTION = (
    (Decimal("16"), "Très Bien"),
    (Decimal("14"), "Bien"),
    (Decimal("12"), "Assez Bien"),
    (Decimal("10"), "Passable"),
)


# ============================================================
# SEUILS D'APPRÉCIATION PAR MATIÈRE
# ============================================================
# Utilisés pour la colonne "Appréciation" de chaque matière
# dans le bulletin. Ajuste librement selon les usages de ton école.

SEUILS_APPRECIATION_MATIERE = (
    (Decimal("16"), "Excellent"),
    (Decimal("14"), "Très Bien"),
    (Decimal("12"), "Bien"),
    (Decimal("10"), "Assez Bien"),
    (Decimal("8"), "Passable"),
    (Decimal("5"), "Médiocre"),
    (Decimal("3"), "Faible"),
)


def determiner_appreciation_matiere(moyenne):
    for seuil, libelle in SEUILS_APPRECIATION_MATIERE:
        if moyenne >= seuil:
            return libelle
    return "Insuffisant"


def determiner_mention(moyenne):
    for seuil, libelle in SEUILS_MENTION:
        if moyenne >= seuil:
            return libelle
    return "Insuffisant"


def determiner_decision(moyenne):
    return "ADMIS" if moyenne >= Decimal("10") else "REDOUBLE"


def _valeur_note(note_obj):
    """Une note d'élève absent compte pour 0."""
    return Decimal("0") if note_obj.absent else note_obj.note


# ============================================================
# ÉTAPE 1 : MOYENNE PAR MATIÈRE (SubjectResult)
# ============================================================

def calculer_resultat_matiere(eleve, assignment, period):
    """
    Calcule et enregistre le SubjectResult d'un élève pour une
    affectation (matière/classe/enseignant) et une période données.
    """

    notes = (
        Note.objects
        .filter(
            eleve=eleve,
            evaluation__assignment=assignment,
            evaluation__period=period,
            is_deleted=False,
        )
        .select_related("evaluation")
    )

    interros = [n for n in notes if n.evaluation.evaluation_type == "INTERROGATION"]
    devoirs = {n.evaluation.numero: n for n in notes if n.evaluation.evaluation_type == "DEVOIR"}

    if interros:
        moyenne_interros = sum((_valeur_note(n) for n in interros), Decimal("0")) / Decimal(len(interros))
    else:
        moyenne_interros = Decimal("0")

    devoir_1 = _valeur_note(devoirs[1]) if 1 in devoirs else Decimal("0")
    devoir_2 = _valeur_note(devoirs[2]) if 2 in devoirs else Decimal("0")

    moyenne = (moyenne_interros + devoir_1 + devoir_2) / Decimal("3")
    coefficient = assignment.coefficient
    points = moyenne * coefficient

    resultat, _ = SubjectResult.objects.update_or_create(
        eleve=eleve,
        assignment=assignment,
        period=period,
        defaults={
            "moyenne_interrogations": moyenne_interros.quantize(Decimal("0.01")),
            "devoir_1": devoir_1,
            "devoir_2": devoir_2,
            "moyenne": moyenne.quantize(Decimal("0.01")),
            "coefficient": coefficient,
            "points": points.quantize(Decimal("0.01")),
            "appreciation": determiner_appreciation_matiere(moyenne),
        },
    )
    return resultat


def classer_matiere(assignment, period):
    """Attribue le rang de chaque élève au sein d'une matière/classe."""

    resultats = list(
        SubjectResult.objects
        .filter(assignment=assignment, period=period)
        .order_by("-moyenne")
    )

    rang_actuel = 0
    moyenne_precedente = None

    for i, resultat in enumerate(resultats, start=1):
        if resultat.moyenne != moyenne_precedente:
            rang_actuel = i
            moyenne_precedente = resultat.moyenne
        resultat.rang = rang_actuel

    SubjectResult.objects.bulk_update(resultats, ["rang"])


# ============================================================
# ÉTAPE 2 : MOYENNE GÉNÉRALE DE L'ÉLÈVE (StudentResult)
# ============================================================

def calculer_resultat_eleve(eleve, period):
    """
    Agrège les SubjectResult d'un élève pour une période
    et enregistre son StudentResult (moyenne générale, mention, décision).

    N'écrit JAMAIS conduite/felicitations/encouragements/tableau_honneur/
    avertissement/blame/travail_acceptable/heures_absence : ces champs sont
    saisis manuellement par le staff et ne doivent pas être écrasés ici.
    """

    subject_results = list(
        SubjectResult.objects
        .filter(eleve=eleve, period=period)
        .select_related("assignment__subject")
    )

    total_points = sum((r.points for r in subject_results), Decimal("0"))
    total_coefficients = sum((r.coefficient for r in subject_results), 0)

    if total_coefficients:
        moyenne_generale = total_points / Decimal(total_coefficients)
    else:
        moyenne_generale = Decimal("0")

    moyenne_generale = moyenne_generale.quantize(Decimal("0.01"))

    def moyenne_ponderee(resultats):
        pts = sum((r.points for r in resultats), Decimal("0"))
        coef = sum((r.coefficient for r in resultats), 0)
        if not coef:
            return Decimal("0")
        return (pts / Decimal(coef)).quantize(Decimal("0.01"))

    resultats_scientifiques = [
        r for r in subject_results
        if r.assignment.subject.categorie == "scientifique"
    ]
    resultats_litteraires = [
        r for r in subject_results
        if r.assignment.subject.categorie == "litteraire"
    ]

    moyenne_scientifique = moyenne_ponderee(resultats_scientifiques)
    moyenne_litteraire = moyenne_ponderee(resultats_litteraires)

    resultat, _ = StudentResult.objects.update_or_create(
        eleve=eleve,
        period=period,
        defaults={
            "total_points": total_points.quantize(Decimal("0.01")),
            "total_coefficients": total_coefficients,
            "moyenne_generale": moyenne_generale,
            "moyenne_scientifique": moyenne_scientifique,
            "moyenne_litteraire": moyenne_litteraire,
            "mention": determiner_mention(moyenne_generale),
            "decision": determiner_decision(moyenne_generale),
        },
    )
    return resultat


def classer_eleves(classe, period):
    """Attribue le rang général de chaque élève au sein de sa classe."""

    resultats = list(
        StudentResult.objects
        .filter(eleve__classe=classe, period=period)
        .order_by("-moyenne_generale")
    )

    rang_actuel = 0
    moyenne_precedente = None

    for i, resultat in enumerate(resultats, start=1):
        if resultat.moyenne_generale != moyenne_precedente:
            rang_actuel = i
            moyenne_precedente = resultat.moyenne_generale
        resultat.rang = rang_actuel

    StudentResult.objects.bulk_update(resultats, ["rang"])


# ============================================================
# ÉTAPE 3 : CALCUL COMPLET POUR UNE CLASSE / UNE PÉRIODE
# ============================================================

@transaction.atomic
def calculer_resultats_classe(classe, period):
    """
    Point d'entrée principal : recalcule tout (matières + moyenne
    générale + classements) pour une classe et une période données.
    À appeler depuis la vue "calculer_resultats".
    """

    school_year = period.school_year

    assignments = Assignment.objects.filter(
        classe=classe,
        school_year=school_year,
        active=True,
    )

    eleves = Eleve.objects.filter(classe=classe)

    # 1. Moyenne par matière, pour chaque élève et chaque affectation
    for assignment in assignments:
        for eleve in eleves:
            calculer_resultat_matiere(eleve, assignment, period)
        classer_matiere(assignment, period)

    # 2. Moyenne générale de chaque élève
    for eleve in eleves:
        calculer_resultat_eleve(eleve, period)

    # 3. Classement général de la classe
    classer_eleves(classe, period)