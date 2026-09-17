"""
===========================================================
ESAIE ACADEMY

Application : Library

Signals

===========================================================
"""

from django.db.models.signals import (
    post_save,
    post_delete,
)

from django.dispatch import receiver

from django.db.models import Avg

from .models import *

# ==========================================================
# BOOKMARK
# ==========================================================

@receiver(post_save, sender=LibraryBookmark)
def bookmark_created(sender, instance, created, **kwargs):

    if created:

        LibraryHistory.objects.create(

            student=instance.student,

            book=instance.book,

            chapter=instance.chapter,

            action="bookmark",

            page=instance.page

        )

# ==========================================================
# FAVORITE
# ==========================================================

@receiver(post_save, sender=LibraryFavorite)
def favorite_created(sender, instance, created, **kwargs):

    if created:

        book = instance.book

        book.total_favorites += 1

        book.save(
            update_fields=["total_favorites"]
        )


@receiver(post_delete, sender=LibraryFavorite)
def favorite_deleted(sender, instance, **kwargs):

    book = instance.book

    if book.total_favorites > 0:

        book.total_favorites -= 1

        book.save(
            update_fields=["total_favorites"]
        )

# ==========================================================
# DOWNLOAD
# ==========================================================

@receiver(post_save, sender=LibraryDownload)
def download_created(sender, instance, created, **kwargs):

    if created:

        book = instance.book

        book.total_downloads += 1

        book.save(
            update_fields=["total_downloads"]
        )

# ==========================================================
# HISTORY
# ==========================================================

@receiver(post_save, sender=LibraryHistory)
def history_created(sender, instance, created, **kwargs):

    if created:

        book = instance.book

        book.total_reads += 1

        book.save(
            update_fields=["total_reads"]
        )

# ==========================================================
# RATING
# ==========================================================

@receiver(post_save, sender=LibraryRating)
def rating_created(sender, instance, created, **kwargs):

    ratings = LibraryRating.objects.filter(
        book=instance.book
    )

    average = ratings.aggregate(
        avg=Avg("rating")
    )["avg"] or 0

    instance.book.average_rating = average

    instance.book.total_ratings = ratings.count()

    instance.book.save(
        update_fields=[
            "average_rating",
            "total_ratings"
        ]
    )
 # ==========================================================
# REVIEW
# ==========================================================

@receiver(post_save, sender=LibraryReview)
def review_created(sender, instance, created, **kwargs):

    if created:

        instance.book.total_comments += 1

        instance.book.save(
            update_fields=["total_comments"]
        )


# ==========================================================
# READING PROGRESS
# ==========================================================

@receiver(post_save, sender=LibraryReadingProgress)
def reading_progress_saved(sender, instance, created, **kwargs):

    if instance.completed:

        LibraryCertificate.objects.get_or_create(

            student=instance.student,

            book=instance.book,

            defaults={

                "certificate_number":

                f"CERT-{instance.student.id}-{instance.book.id}"

            }

        )


# ==========================================================
# BORROW
# ==========================================================

@receiver(post_save, sender=LibraryBorrow)
def borrow_created(sender, instance, created, **kwargs):

    if created:

        LibraryHistory.objects.create(

            student=instance.student,

            book=instance.book,

            action="borrow"

        )


# ==========================================================
# RESERVATION
# ==========================================================

@receiver(post_save, sender=LibraryReservation)
def reservation_created(sender, instance, created, **kwargs):

    if created:

        LibraryHistory.objects.create(

            student=instance.student,

            book=instance.book,

            action="reservation"

        )
           