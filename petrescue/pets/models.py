from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class PetReport(models.Model):
    SPECIES_CHOICES = [
        ("dog", "Dog"),
        ("cat", "Cat"),
        ("bird", "Bird"),
        ("other", "Other"),
    ]

    STATUS_CHOICES = [
        ("found", "Found"),
        ("claimed", "Claimed"),
        ("closed", "Closed"),
    ]

    reporter = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="pet_reports"
    )
    pet_name = models.CharField(max_length=120, blank=True)
    species = models.CharField(max_length=20, choices=SPECIES_CHOICES)
    breed = models.CharField(max_length=120, blank=True)
    color = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)
    contact_name = models.CharField(max_length=120, blank=True, default="")
    contact_email = models.EmailField(blank=True, default="")
    contact_phone = models.CharField(max_length=40, blank=True, default="")
    location_found = models.CharField(max_length=255)
    date_found = models.DateField()
    photo = models.ImageField(upload_to="pet_photos/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="found")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["species", "color"]),
            models.Index(fields=["status", "date_found"]),
        ]

    def __str__(self) -> str:  # noqa: D401
        return f"{self.get_species_display()} - {self.color or 'Unknown'} @ {self.location_found}"


class Claim(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    pet = models.ForeignKey(PetReport, on_delete=models.CASCADE, related_name="claims")
    claimer_name = models.CharField(max_length=120)
    claimer_email = models.EmailField()
    claimer_phone = models.CharField(max_length=40, blank=True)
    message = models.TextField(blank=True)
    proof_photo = models.ImageField(upload_to="claim_proofs/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    reviewed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="reviewed_claims"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["pet", "claimer_email"],
                name="unique_claim_per_pet_email",
            )
        ]

    def __str__(self) -> str:  # noqa: D401
        return f"Claim for {self.pet_id} by {self.claimer_email} ({self.status})"


# Create your models here.
