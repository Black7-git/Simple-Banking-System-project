from django.contrib import admin
from .models import Pet, PetImage, PetRequest

class PetImageInline(admin.TabularInline):
    """Inline admin for pet images"""
    model = PetImage
    extra = 1

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    """Admin configuration for Pet model"""
    list_display = ('name', 'pet_type', 'breed', 'status', 'found_location', 'found_date', 'reported_by', 'is_verified')
    list_filter = ('pet_type', 'status', 'size', 'gender', 'is_verified', 'created_at')
    search_fields = ('name', 'breed', 'color', 'found_location', 'description')
    date_hierarchy = 'created_at'
    inlines = [PetImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'pet_type', 'breed', 'color', 'size', 'age_estimate', 'gender')
        }),
        ('Description', {
            'fields': ('description', 'distinctive_features')
        }),
        ('Location & Status', {
            'fields': ('status', 'found_location', 'found_date', 'current_location')
        }),
        ('Contact Information', {
            'fields': ('reported_by', 'contact_phone', 'contact_email')
        }),
        ('Administrative', {
            'fields': ('is_verified',)
        }),
    )

@admin.register(PetRequest)
class PetRequestAdmin(admin.ModelAdmin):
    """Admin configuration for PetRequest model"""
    list_display = ('request_type', 'pet', 'requester', 'status', 'created_at')
    list_filter = ('request_type', 'status', 'created_at')
    search_fields = ('requester__username', 'pet__name', 'message')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Request Details', {
            'fields': ('request_type', 'pet', 'requester', 'message')
        }),
        ('Status', {
            'fields': ('status', 'reviewed_by', 'admin_notes')
        }),
    )
