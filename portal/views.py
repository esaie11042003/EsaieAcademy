from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from configuration.models import SchoolStaff
from students.models import Eleve


def accueil(request):
    return render(request, "portal/accueil.html")


@login_required
def dashboard(request):
    """
    Redirige l'utilisateur vers le dashboard correspondant
    à son rôle (élève, enseignant, parent, staff, admin).
    """
    if request.user.is_superuser:
        return redirect("platform_admin:vue_ensemble")

    role = request.user.role
    if role == "student":
        return render(request, "portal/dashboard_student.html")

    elif role == "teacher":
        return render(request, "portal/dashboard_teacher.html")

    elif role == "parent":
        return render(request, "portal/dashboard_parent.html", {
            "enfants": request.user.enfants.all()
        })

    elif role == "staff":
        school_staff = SchoolStaff.objects.filter(user=request.user).select_related("school", "role").first()

        context = {"school_staff": school_staff}

        if school_staff:
            school = school_staff.school
            context["school"] = school
            context["etablissement_en_attente"] = school.statut_validation == "en_attente"
            context["etablissement_rejete"] = school.statut_validation == "rejete"

            if school.statut_validation == "valide":
                context["eleves"] = Eleve.objects.filter(classe__school=school).select_related("classe")
                context["administration"] = SchoolStaff.objects.filter(school=school).select_related("user", "role")

        return render(request, "portal/dashboard_staff.html", context)

    elif role == "admin":
        from repetition.models import DemandeMaitreEtude
        from configuration.models import SchoolProfile
        nouvelles_demandes = DemandeMaitreEtude.objects.filter(statut="nouvelle").count()
        etablissements_en_attente = SchoolProfile.objects.filter(statut_validation="en_attente").count()
        return render(request, "portal/dashboard_admin.html", {
            "nouvelles_demandes": nouvelles_demandes,
            "etablissements_en_attente": etablissements_en_attente,
        })

    return render(request, "portal/dashboard_default.html")


def choix_acces(request):
    role = request.GET.get("role", "")
    return render(request, "portal/choix_acces.html", {"role": role})
