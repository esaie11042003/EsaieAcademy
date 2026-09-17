from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from teachers.models import Teacher
from students.models import Eleve
from configuration.models import SchoolStaff
from .forms import EvaluationForm, ModifierNoteForm, SupprimerNoteForm
from .models import Evaluation, Note
from django.shortcuts import get_object_or_404
from django.contrib import messages
from configuration.models import SchoolStaff


def _peut_gerer(user, evaluation):
    """
    Autorisé si l'utilisateur est le professeur de l'affectation,
    ou membre de l'administration de l'établissement concerné.
    """
    teacher = Teacher.objects.filter(user=user).first()
    if teacher and evaluation.assignment.teacher == teacher:
        return True

    school = evaluation.assignment.classe.school
    if school and SchoolStaff.objects.filter(user=user, school=school).exists():
        return True

    return False


@login_required
def gerer_evaluations(request):

    teacher = Teacher.objects.filter(user=request.user).first()
    if not teacher:
        messages.error(request, "Vous devez être enseignant pour accéder à cette page.")
        return redirect("portal:dashboard")

    if request.method == "POST":
        form = EvaluationForm(request.POST, teacher=teacher)
        if form.is_valid():
            evaluation = form.save()
            messages.success(request, "Évaluation créée. Vous pouvez maintenant saisir les notes.")
            return redirect("evaluations:saisir_notes", pk=evaluation.pk)
    else:
        form = EvaluationForm(teacher=teacher)

    evaluations = Evaluation.objects.filter(assignment__teacher=teacher).select_related("assignment", "period")

    return render(request, "evaluations/gerer_evaluations.html", {
        "form": form,
        "evaluations": evaluations,
    })


@login_required
def saisir_notes(request, pk):

    evaluation = get_object_or_404(Evaluation, pk=pk)

    if not _peut_gerer(request.user, evaluation):
        messages.error(request, "Vous n'êtes pas autorisé à saisir les notes de cette évaluation.")
        return redirect("portal:dashboard")

    eleves = Eleve.objects.filter(classe=evaluation.assignment.classe).order_by("nom", "prenom")

    deja_notes_ids = set(
        Note.objects.filter(evaluation=evaluation, is_deleted=False).values_list("eleve_id", flat=True)
    )
    eleves_sans_note = [e for e in eleves if e.pk not in deja_notes_ids]

    if request.method == "POST":
        for eleve in eleves_sans_note:
            note_valeur = request.POST.get(f"note_{eleve.pk}", "").strip()
            absent = request.POST.get(f"absent_{eleve.pk}") == "on"

            if not note_valeur and not absent:
                continue

            Note.objects.create(
                evaluation=evaluation,
                eleve=eleve,
                note=note_valeur if note_valeur else 0,
                absent=absent,
            )

        messages.success(request, "Notes enregistrées avec succès.")
        return redirect("evaluations:liste_notes", pk=evaluation.pk)

    return render(request, "evaluations/saisir_notes.html", {
        "evaluation": evaluation,
        "eleves": eleves_sans_note,
    })


@login_required
def liste_notes(request, pk):

    evaluation = get_object_or_404(Evaluation, pk=pk)

    if not _peut_gerer(request.user, evaluation):
        messages.error(request, "Vous n'êtes pas autorisé à consulter les notes de cette évaluation.")
        return redirect("portal:dashboard")

    notes = Note.objects.filter(evaluation=evaluation, is_deleted=False).select_related("eleve").order_by("eleve__nom")

    return render(request, "evaluations/liste_notes.html", {
        "evaluation": evaluation,
        "notes": notes,
    })


@login_required
def modifier_note(request, pk):

    note = get_object_or_404(Note, pk=pk, is_deleted=False)
    evaluation = note.evaluation

    if not _peut_gerer(request.user, evaluation):
        messages.error(request, "Vous n'êtes pas autorisé à modifier cette note.")
        return redirect("portal:dashboard")

    if request.method == "POST":
        form = ModifierNoteForm(request.POST)
        if form.is_valid():
            note.note = form.cleaned_data["note"]
            note.absent = form.cleaned_data["absent"]
            note.modified_by = request.user
            note.modification_reason = form.cleaned_data["raison"]
            note.save()
            messages.success(request, "Note modifiée avec succès.")
            return redirect("evaluations:liste_notes", pk=evaluation.pk)
    else:
        form = ModifierNoteForm(initial={"note": note.note, "absent": note.absent})

    return render(request, "evaluations/modifier_note.html", {
        "form": form,
        "note": note,
    })


@login_required
def supprimer_note(request, pk):

    note = get_object_or_404(Note, pk=pk, is_deleted=False)
    evaluation = note.evaluation

    if not _peut_gerer(request.user, evaluation):
        messages.error(request, "Vous n'êtes pas autorisé à supprimer cette note.")
        return redirect("portal:dashboard")

    if request.method == "POST":
        form = SupprimerNoteForm(request.POST)
        if form.is_valid():
            note.is_deleted = True
            note.deleted_by = request.user
            note.deleted_at = timezone.now()
            note.deletion_reason = form.cleaned_data["raison"]
            note.save()
            messages.success(request, "Note supprimée avec succès.")
            return redirect("evaluations:liste_notes", pk=evaluation.pk)
    else:
        form = SupprimerNoteForm()

    return render(request, "evaluations/supprimer_note.html", {
        "form": form,
        "note": note,
    })
@login_required
def suivi_ecole(request):

    school_staff = SchoolStaff.objects.filter(user=request.user).select_related("school").first()

    if not school_staff:
        messages.error(request, "Accès réservé au personnel d'un établissement.")
        return redirect("portal:dashboard")

    school = school_staff.school

    evaluations = Evaluation.objects.filter(
        assignment__classe__school=school
    ).select_related("assignment__subject", "assignment__classe", "assignment__teacher__user", "period")

    return render(request, "evaluations/suivi_ecole.html", {
        "school": school,
        "evaluations": evaluations,
    })


@login_required
def historique_evaluation(request, pk):

    evaluation = get_object_or_404(Evaluation, pk=pk)
    school_staff = SchoolStaff.objects.filter(user=request.user, school=evaluation.assignment.classe.school).first()

    if not school_staff:
        messages.error(request, "Vous n'êtes pas autorisé à consulter cet historique.")
        return redirect("portal:dashboard")

    notes_actives = Note.objects.filter(evaluation=evaluation, is_deleted=False).select_related("eleve", "modified_by")
    notes_modifiees = notes_actives.exclude(modified_by__isnull=True)
    notes_supprimees = Note.objects.filter(evaluation=evaluation, is_deleted=True).select_related("eleve", "deleted_by")

    return render(request, "evaluations/historique_evaluation.html", {
        "evaluation": evaluation,
        "notes_actives": notes_actives,
        "notes_modifiees": notes_modifiees,
        "notes_supprimees": notes_supprimees,
    })