from django.db import models
from django.utils import timezone
from django.urls import reverse
import uuid


class PetSpecies(models.TextChoices):
    DOG = "dog", "Dog"
    CAT = "cat", "Cat"
    BIRD = "bird", "Bird"
    OTHER = "other", "Other"


class ReportType(models.TextChoices):
    FOUND = "found", "Found"
    LOST = "lost", "Lost"


class ReportStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PUBLISHED = "published", "Published"
    MATCHED = "matched", "Matched"
    RESOLVED = "resolved", "Resolved"
    ARCHIVED = "archived", "Archived"


def pet_photo_upload_path(instance: "PetReport", filename: str) -> str:
    return f"pet_photos/{instance.reference_code}/{filename}"


class PetReport(models.Model):
    reference_code = models.CharField(
        max_length=12,
        unique=True,
        editable=False,
        db_index=True,
        help_text="Public code to check this report's status.",
    )
    report_type = models.CharField(
        max_length=16, choices=ReportType.choices, db_index=True
    )
    status = models.CharField(
        max_length=16, choices=ReportStatus.choices, default=ReportStatus.PENDING, db_index=True
    )

    species = models.CharField(max_length=16, choices=PetSpecies.choices, db_index=True)
    breed = models.CharField(max_length=120, blank=True)
    color = models.CharField(max_length=120, blank=True, db_index=True)
    distinctive_marks = models.CharField(max_length=255, blank=True)

    location = models.CharField(max_length=200, help_text="Area where pet was lost/found")
    date_seen = models.DateField(help_text="Date pet was lost/found", db_index=True)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to=pet_photo_upload_path, blank=True, null=True)

    reporter_name = models.CharField(max_length=120)
    reporter_email = models.EmailField()
    reporter_phone = models.CharField(max_length=40, blank=True)

    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["report_type", "species", "color"]),
            models.Index(fields=["status", "date_seen"]),
        ]

    def save(self, *args, **kwargs):
        if not self.reference_code:
            # Generate short, user-friendly code
            self.reference_code = uuid.uuid4().hex[:10].upper()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.get_report_type_display()} {self.get_species_display()} ({self.reference_code})"

    def get_absolute_url(self):
        return reverse("pets:report_detail", args=[self.reference_code])

# Create your models here.
