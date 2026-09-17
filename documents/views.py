from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .forms import DocumentForm
from .models import Document, DocumentFile, DocumentCategory, DocumentType
from classes.models import Classe
from django.utils import timezone
from datetime import timedelta


def liste_documents(request):
    query = request.GET.get("q", "").strip()

    documents = (
        Document.objects
        .filter(published=True)
        .select_related("category", "document_type")
        .prefetch_related("files")
    )

    if query:
        documents = documents.filter(
            Q(title__icontains=query)
            | Q(category__name__icontains=query)
            | Q(description__icontains=query)
        )

    for doc in documents:
        doc.a_acces = _a_acces(request.user, doc)

    return render(
        request,
        "documents/liste.html",
        {
            "documents": documents,
            "query": query,
        },
    )


@login_required
def ajouter_document(request):
    if request.user.role != "admin":
        messages.error(
            request,
            "Accès réservé aux administrateurs de la plateforme."
        )
        return redirect("documents:liste_documents")

    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            document = form.save(commit=False)

            # Création d'un slug unique
            base_slug = slugify(document.title)
            slug = base_slug
            i = 1

            while Document.objects.filter(slug=slug).exists():
                i += 1
                slug = f"{base_slug}-{i}"

            document.slug = slug
            document.published = True
            document.publication_date = timezone.now()
            document.save()

            # Fichier principal
            fichier = form.cleaned_data["fichier"]

            DocumentFile.objects.create(
                document=document,
                file_type=document.document_type,
                title=document.title,
                file=fichier,
                file_size=fichier.size,
                is_main_file=True,
            )

            # Fichier corrigé
            categories_avec_corrige = [
                "TD",
                "DEVOIR",
                "INTERROGATION",
            ]

            fichier_corrige = form.cleaned_data.get("fichier_corrige")

            if (
                fichier_corrige
                and document.category.code in categories_avec_corrige
            ):
                DocumentFile.objects.create(
                    document=document,
                    file_type=document.document_type,
                    title=f"Corrigé — {document.title}",
                    file=fichier_corrige,
                    file_size=fichier_corrige.size,
                    is_main_file=False,
                )

            messages.success(
                request,
                "Document ajouté avec succès."
            )

            return redirect("documents:liste_documents")

    else:
        form = DocumentForm()

    return render(
        request,
        "documents/ajouter_document.html",
        {"form": form},
    )


@login_required
def gerer_corrige(request, pk):
    document = get_object_or_404(Document, pk=pk)

    if request.user.role != "admin":
        messages.error(
            request,
            "Accès réservé aux administrateurs de la plateforme."
        )
        return redirect("documents:liste_documents")

    if request.method == "POST":
        fichier_corrige = request.FILES.get("fichier_corrige")

        if fichier_corrige:
            # Supprimer l'ancien corrigé
            DocumentFile.objects.filter(
                document=document,
                is_main_file=False
            ).delete()

            # Ajouter le nouveau corrigé
            DocumentFile.objects.create(
                document=document,
                file_type=document.document_type,
                title=f"Corrigé — {document.title}",
                file=fichier_corrige,
                file_size=fichier_corrige.size,
                is_main_file=False,
            )

            messages.success(
                request,
                "Corrigé mis à jour avec succès."
            )

            return redirect("documents:liste_documents")

    return render(
        request,
        "documents/gerer_corrige.html",
        {"document": document},
    )


@login_required
def modifier_document(request, pk):
    document = get_object_or_404(Document, pk=pk)

    if request.user.role != "admin":
        messages.error(
            request,
            "Accès réservé aux administrateurs de la plateforme."
        )
        return redirect("documents:liste_documents")

    if request.method == "POST":
        document.title = request.POST.get(
            "title",
            document.title
        )

        category_id = request.POST.get("category")
        document_type_id = request.POST.get("document_type")
        classe_id = request.POST.get("classe")

        if category_id:
            document.category_id = category_id

        if document_type_id:
            document.document_type_id = document_type_id

        document.classe_id = classe_id or None

        document.access_type = request.POST.get("access_type")
        document.prix = request.POST.get("prix") or None

        document.save()

        messages.success(
            request,
            "Document mis à jour avec succès."
        )

        return redirect("documents:liste_documents")

    categories = DocumentCategory.objects.all()
    types = DocumentType.objects.all()
    classes = Classe.objects.all()

    return render(
        request,
        "documents/modifier_document.html",
        {
            "document": document,
            "categories": categories,
            "types": types,
            "classes": classes,
        },
    )


def _a_acces(user, document):
    # Documents gratuits
    if document.access_type != "paid" or not document.prix:
        return True

    # Les administrateurs ont toujours accès
    if user.is_authenticated and user.role == "admin":
        return True

    # Utilisateur non connecté
    if not user.is_authenticated:
        return False

    from monetisation.models import Purchase

    ct = ContentType.objects.get_for_model(document)

    return Purchase.objects.filter(
        content_type=ct,
        object_id=document.pk,
        acheteur=user,
        statut="VALIDE",
    ).exists()


@login_required
def telecharger(request, pk, file_id):
    document = get_object_or_404(Document, pk=pk)

    fichier = get_object_or_404(
        DocumentFile,
        pk=file_id,
        document=document,
    )

    if not _a_acces(request.user, document):
        messages.error(
            request,
            "Vous devez payer ce document pour le télécharger."
        )

        ct = ContentType.objects.get_for_model(document)

        return redirect(
            "monetisation:acheter",
            app_label=ct.app_label,
            model_name=ct.model,
            pk=document.pk,
        )

    return redirect(fichier.file.url)


@login_required
def basculer_document(request, pk):
    if request.user.role != "admin":
        messages.error(
            request,
            "Accès réservé aux administrateurs de la plateforme."
        )
        return redirect("documents:liste_documents")

    document = get_object_or_404(Document, pk=pk)

    document.published = not document.published
    document.save()

    if document.published:
        messages.success(
            request,
            f"« {document.title} » est de nouveau visible sur la plateforme."
        )
    else:
        messages.success(
            request,
            f"« {document.title} » a été désactivé — "
            "visible uniquement par les admins."
        )

    return redirect("documents:liste_documents")

@login_required
def supprimer_document(request, pk):

    if request.user.role != "admin":
        messages.error(request, "Accès réservé aux administrateurs de la plateforme.")
        return redirect("documents:liste_documents")

    document = get_object_or_404(Document, pk=pk)

    if request.method == "POST":
        document.is_deleted = True
        document.deleted_at = timezone.now()
        document.published = False
        document.save()
        messages.success(request, f"« {document.title} » a été déplacé vers la corbeille (suppression définitive dans 30 jours).")
        return redirect("documents:liste_documents")

    return render(request, "documents/supprimer_document.html", {"document": document})


@login_required
def corbeille(request):

    if request.user.role != "admin":
        messages.error(request, "Accès réservé aux administrateurs de la plateforme.")
        return redirect("documents:liste_documents")

    limite = timezone.now() - timedelta(days=30)
    Document.objects.filter(is_deleted=True, deleted_at__lt=limite).delete()

    documents = Document.objects.filter(is_deleted=True).select_related("category", "document_type")
    for doc in documents:
        jours_restants = 30 - (timezone.now() - doc.deleted_at).days
        doc.jours_restants = max(jours_restants, 0)

    return render(request, "documents/corbeille.html", {"documents": documents})


@login_required
def restaurer_document(request, pk):

    if request.user.role != "admin":
        messages.error(request, "Accès réservé aux administrateurs de la plateforme.")
        return redirect("documents:liste_documents")

    document = get_object_or_404(Document, pk=pk, is_deleted=True)
    document.is_deleted = False
    document.deleted_at = None
    document.save()
    messages.success(request, f"« {document.title} » a été restauré.")
    return redirect("documents:corbeille")


@login_required
def supprimer_definitivement(request, pk):

    if request.user.role != "admin":
        messages.error(request, "Accès réservé aux administrateurs de la plateforme.")
        return redirect("documents:liste_documents")

    document = get_object_or_404(Document, pk=pk, is_deleted=True)
    titre = document.title
    document.delete()
    messages.success(request, f"« {titre} » a été supprimé définitivement.")
    return redirect("documents:corbeille")


@login_required
def documents_desactives(request):

    if request.user.role != "admin":
        messages.error(request, "Accès réservé aux administrateurs de la plateforme.")
        return redirect("documents:liste_documents")

    documents = Document.objects.filter(published=False, is_deleted=False).select_related("category", "document_type")

    return render(request, "documents/documents_desactives.html", {"documents": documents})