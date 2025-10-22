"""
Django admin configuration for PetRescue models
"""
from django.contrib import admin
from .models import UserProfile, Pet, Request, Notification, Comment


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'is_admin', 'created_at']
    list_filter = ['is_admin', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ['name', 'pet_type', 'status', 'location_found', 'date_found', 'reported_by', 'is_verified', 'created_at']
    list_filter = ['status', 'pet_type', 'size', 'is_verified', 'created_at']
    search_fields = ['name', 'breed', 'color', 'location_found', 'reported_by__username']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'pet_type', 'breed', 'color', 'size', 'age_approximate')
        }),
        ('Physical Characteristics', {
            'fields': ('distinctive_marks',)
        }),
        ('Status and Location', {
            'fields': ('status', 'location_found', 'date_found')
        }),
        ('Contact Information', {
            'fields': ('reported_by', 'contact_phone', 'contact_email')
        }),
        ('Media', {
            'fields': ('photo',)
        }),
        ('Additional Information', {
            'fields': ('additional_info',)
        }),
        ('Verification', {
            'fields': ('is_verified', 'verified_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ['subject', 'request_type', 'requester', 'status', 'created_at', 'resolved_at']
    list_filter = ['request_type', 'status', 'created_at']
    search_fields = ['subject', 'description', 'requester__username']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Request Information', {
            'fields': ('request_type', 'pet', 'requester', 'subject', 'description')
        }),
        ('Status', {
            'fields': ('status', 'admin_notes', 'resolved_by', 'resolved_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['title', 'message', 'user__username']
    date_hierarchy = 'created_at'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['pet', 'user', 'content', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'user__username', 'pet__name']
    date_hierarchy = 'created_at'
