from django.contrib import admin
from .models import PetReport


@admin.register(PetReport)
class PetReportAdmin(admin.ModelAdmin):
    list_display = (
        "reference_code",
        "report_type",
        "status",
        "species",
        "color",
        "location",
        "date_seen",
        "created_at",
    )
    list_filter = ("report_type", "status", "species", "date_seen", "created_at")
    search_fields = (
        "reference_code",
        "reporter_name",
        "reporter_email",
        "breed",
        "color",
        "location",
        "description",
    )
    readonly_fields = ("reference_code", "created_at", "updated_at")

# Register your models here.
