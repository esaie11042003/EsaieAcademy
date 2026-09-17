from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import HttpResponse

from configuration.models import SchoolStaff
from classes.models import Classe
from school.models import Period
from students.models import Eleve
from platform_admin.models import PlatformBranding

from .models import SubjectResult, StudentResult
from .services import calculer_resultats_classe
from .forms import ConduiteForm


# ============================================================
# Correspondance couleur choisie par la classe -> code hexadécimal
# ============================================================

COULEURS_HEX = {
    "bleu": "#0b3d91",
    "orange": "#e67e22",
    "rouge": "#c0392b",
    "vert": "#1e7d34",
    "violet": "#6c3483",
    "noir": "#222222",
}

# Correspondance style de bordure (1 à 4) -> propriété CSS border-style

STYLES_BORDURE_CSS = {
    1: "solid",
    2: "double",
    3: "groove",
    4: "ridge",
}


def _staff_autorise(request, school):
    """Vrai si l'utilisateur est admin plateforme ou staff de cette école."""
    if request.user.role == "admin":
        return True
    return SchoolStaff.objects.filter(user=request.user, school=school).exists()


@login_required
def choisir_resultats(request):
    """
    Point d'entrée depuis le dashboard staff : l'utilisateur choisit
    une classe et une période, puis est redirigé vers liste_resultats.
    """

    school_staff = SchoolStaff.objects.filter(user=request.user).select_related("school").first()

    if not school_staff and request.user.role != "admin":
        messages.error(request, "Vous devez d'abord créer ou rejoindre un établissement.")
        return redirect("portal:dashboard")

    school = school_staff.school if school_staff else None

    if school is not None:
        classes = Classe.objects.filter(school=school)
    else:
        classes = Classe.objects.all()

    periods = Period.objects.select_related("school_year").order_by("-school_year__date_debut", "start_date")

    classe_id = request.GET.get("classe_id")
    period_id = request.GET.get("period_id")

    if classe_id and period_id:
        return redirect("results:liste_resultats", classe_id=classe_id, period_id=period_id)

    return render(request, "results/choisir_resultats.html", {
        "classes": classes,
        "periods": periods,
    })


@login_required
def calculer_resultats(request, classe_id, period_id):

    classe = get_object_or_404(Classe, pk=classe_id)
    period = get_object_or_404(Period, pk=period_id)

    if not _staff_autorise(request, classe.school):
        messages.error(request, "Vous n'êtes pas autorisé à calculer les résultats de cette classe.")
        return redirect("portal:dashboard")

    calculer_resultats_classe(classe, period)

    messages.success(
        request,
        f"Résultats recalculés pour {classe.nom} — {period.get_name_display()}."
    )
    return redirect("results:liste_resultats", classe_id=classe.pk, period_id=period.pk)


@login_required
def liste_resultats(request, classe_id, period_id):

    classe = get_object_or_404(Classe, pk=classe_id)
    period = get_object_or_404(Period, pk=period_id)

    if not _staff_autorise(request, classe.school):
        messages.error(request, "Vous n'êtes pas autorisé à consulter les résultats de cette classe.")
        return redirect("portal:dashboard")

    resultats = (
        StudentResult.objects
        .filter(eleve__classe=classe, period=period)
        .select_related("eleve")
        .order_by("rang")
    )

    return render(request, "results/liste_resultats.html", {
        "classe": classe,
        "period": period,
        "resultats": resultats,
    })


def _construire_contexte_bulletin(eleve, period):

    subject_results = (
        SubjectResult.objects
        .filter(eleve=eleve, period=period)
        .select_related("assignment__subject", "assignment__teacher__user")
        .order_by("assignment__subject__nom")
    )

    student_result = StudentResult.objects.filter(eleve=eleve, period=period).first()

    classe = eleve.classe
    school = classe.school if classe else None

    effectif_classe = Eleve.objects.filter(classe=classe).count() if classe else 0

    professeur_principal = classe.professeur_principal if classe else None

    directeur = None
    if school:
        directeur = (
            SchoolStaff.objects
            .filter(school=school, role__nom="Directeur", actif=True)
            .select_related("user", "role")
            .first()
        )

    couleur_bulletin = classe.couleur_bulletin if classe else "bleu"
    style_bordure = classe.style_bordure if classe else 1

    branding = PlatformBranding.get_solo()

    return {
        "eleve": eleve,
        "period": period,
        "subject_results": subject_results,
        "student_result": student_result,
        "school": school,
        "effectif_classe": effectif_classe,
        "professeur_principal": professeur_principal,
        "directeur": directeur,
        "logo_devise_benin": branding.logo_devise_benin,
        "couleur_hex": COULEURS_HEX.get(couleur_bulletin, "#0b3d91"),
        "style_bordure_css": STYLES_BORDURE_CSS.get(style_bordure, "solid"),
    }


def _eleve_ou_staff_autorise(request, eleve):
    """
    Autorisé si : admin plateforme, staff de l'école de l'élève,
    l'élève lui-même, ou un parent lié à cet élève.
    """
    if request.user.role == "admin":
        return True
    if eleve.user_id and eleve.user_id == request.user.id:
        return True
    if eleve.parents.filter(pk=request.user.pk).exists():
        return True
    if eleve.classe and eleve.classe.school:
        return SchoolStaff.objects.filter(user=request.user, school=eleve.classe.school).exists()
    return False


@login_required
def bulletins_enfant(request, eleve_id):
    """
    Pour un parent : liste des périodes disponibles pour choisir
    le bulletin de son enfant à consulter.
    """

    eleve = get_object_or_404(Eleve, pk=eleve_id)

    if not _eleve_ou_staff_autorise(request, eleve):
        messages.error(request, "Vous n'êtes pas autorisé à consulter cet élève.")
        return redirect("portal:dashboard")

    periods = Period.objects.select_related("school_year").order_by("-school_year__date_debut", "start_date")

    return render(request, "results/bulletins_enfant.html", {
        "eleve": eleve,
        "periods": periods,
    })


@login_required
def bulletin_eleve(request, eleve_id, period_id):

    eleve = get_object_or_404(Eleve, pk=eleve_id)
    period = get_object_or_404(Period, pk=period_id)

    if not _eleve_ou_staff_autorise(request, eleve):
        messages.error(request, "Vous n'êtes pas autorisé à consulter ce bulletin.")
        return redirect("portal:dashboard")

    contexte = _construire_contexte_bulletin(eleve, period)
    return render(request, "results/bulletin_eleve.html", contexte)


@login_required
def bulletin_pdf(request, eleve_id, period_id):

    # Import local : WeasyPrint peut être lourd à charger, on ne le fait
    # que lorsque le PDF est réellement demandé.
    from weasyprint import HTML

    eleve = get_object_or_404(Eleve, pk=eleve_id)
    period = get_object_or_404(Period, pk=period_id)

    if not _eleve_ou_staff_autorise(request, eleve):
        messages.error(request, "Vous n'êtes pas autorisé à télécharger ce bulletin.")
        return redirect("portal:dashboard")

    contexte = _construire_contexte_bulletin(eleve, period)
    html_string = render_to_string("results/bulletin_pdf.html", contexte)

    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri("/")).write_pdf()

    nom_fichier = f"bulletin_{eleve.matricule or eleve.pk}_{period.name}.pdf"

    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{nom_fichier}"'
    return response


@login_required
def saisir_conduite(request, eleve_id, period_id):
    """
    Formulaire staff pour saisir conduite, récompenses/sanctions
    et heures d'absence. Ces champs ne sont jamais touchés par le
    recalcul automatique des notes (bouton "Recalculer les résultats").
    """

    eleve = get_object_or_404(Eleve, pk=eleve_id)
    period = get_object_or_404(Period, pk=period_id)

    if not eleve.classe or not _staff_autorise(request, eleve.classe.school):
        messages.error(request, "Vous n'êtes pas autorisé à modifier ces informations.")
        return redirect("portal:dashboard")

    student_result, _ = StudentResult.objects.get_or_create(eleve=eleve, period=period)

    if request.method == "POST":
        form = ConduiteForm(request.POST, instance=student_result)
        if form.is_valid():
            form.save()
            messages.success(request, "Conduite et récompenses/sanctions enregistrées.")
            return redirect("results:bulletin_eleve", eleve_id=eleve.pk, period_id=period.pk)
    else:
        form = ConduiteForm(instance=student_result)

    return render(request, "results/conduite_form.html", {
        "form": form,
        "eleve": eleve,
        "period": period,
    })