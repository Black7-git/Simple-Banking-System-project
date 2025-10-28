from django.contrib import admin
from .models import PetReport, Claim


@admin.register(PetReport)
class PetReportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "species",
        "color",
        "location_found",
        "date_found",
        "status",
    )
    list_filter = ("species", "status", "date_found")
    search_fields = ("color", "breed", "location_found", "description")
    actions = ("mark_claimed", "mark_closed")

    @admin.action(description="Mark selected reports as Claimed")
    def mark_claimed(self, request, queryset):
        queryset.update(status="claimed")

    @admin.action(description="Mark selected reports as Closed")
    def mark_closed(self, request, queryset):
        queryset.update(status="closed")


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ("id", "pet", "claimer_email", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("claimer_name", "claimer_email", "message")
    actions = ("approve_claims", "reject_claims")

    @admin.action(description="Approve selected claims")
    def approve_claims(self, request, queryset):
        updated = queryset.update(status="approved")
        # Related reports will be marked claimed via signal on status change
        self.message_user(request, f"Approved {updated} claim(s)")

    @admin.action(description="Reject selected claims")
    def reject_claims(self, request, queryset):
        updated = queryset.update(status="rejected")
        self.message_user(request, f"Rejected {updated} claim(s)")

# Register your models here.
