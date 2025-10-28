from django.contrib import admin
from .models import Notification, PetMatch

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin configuration for Notification model"""
    list_display = ('title', 'recipient', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('title', 'message', 'recipient__username')
    date_hierarchy = 'created_at'

@admin.register(PetMatch)
class PetMatchAdmin(admin.ModelAdmin):
    """Admin configuration for PetMatch model"""
    list_display = ('found_pet', 'lost_pet', 'similarity_score', 'is_confirmed', 'created_at')
    list_filter = ('is_confirmed', 'created_at')
    search_fields = ('found_pet__name', 'lost_pet__name')
    date_hierarchy = 'created_at'
