from django.contrib import admin
from django.utils.html import format_html
from .models import Pet, PetRequest, Notification, UserProfile


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ['pet_type', 'name', 'breed', 'status', 'location_found', 'date_found', 'is_verified']
    list_filter = ['pet_type', 'status', 'is_verified', 'date_found']
    search_fields = ['name', 'breed', 'location_found', 'finder_name']
    readonly_fields = ['date_found', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'pet_type', 'breed', 'color', 'gender', 'age', 'size')
        }),
        ('Status & Location', {
            'fields': ('status', 'location_found', 'date_found', 'description')
        }),
        ('Contact Information', {
            'fields': ('finder_name', 'finder_phone', 'finder_email')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Admin Management', {
            'fields': ('is_verified', 'admin_notes', 'created_by', 'updated_at')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('created_by')


@admin.register(PetRequest)
class PetRequestAdmin(admin.ModelAdmin):
    list_display = ['request_type', 'pet', 'requester_name', 'status', 'created_at', 'processed_by']
    list_filter = ['request_type', 'status', 'created_at']
    search_fields = ['requester_name', 'requester_email', 'pet__name', 'pet__pet_type']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Request Details', {
            'fields': ('request_type', 'pet', 'requester_name', 'requester_phone', 'requester_email')
        }),
        ('Request Information', {
            'fields': ('description', 'proof_of_ownership')
        }),
        ('Status & Processing', {
            'fields': ('status', 'admin_notes', 'processed_by', 'created_at', 'updated_at')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('pet', 'processed_by')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['title', 'message', 'user__username']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'related_pet', 'related_request')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'is_volunteer', 'created_at']
    list_filter = ['is_volunteer', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')