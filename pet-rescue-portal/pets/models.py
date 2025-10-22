"""
Database models for PetRescue application
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    """Extended user profile with additional information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - Profile"


class Pet(models.Model):
    """Model for pet information"""
    PET_STATUS_CHOICES = [
        ('LOST', 'Lost'),
        ('FOUND', 'Found'),
        ('REUNITED', 'Reunited'),
        ('ADOPTED', 'Adopted'),
    ]
    
    PET_TYPE_CHOICES = [
        ('DOG', 'Dog'),
        ('CAT', 'Cat'),
        ('BIRD', 'Bird'),
        ('RABBIT', 'Rabbit'),
        ('OTHER', 'Other'),
    ]
    
    PET_SIZE_CHOICES = [
        ('SMALL', 'Small'),
        ('MEDIUM', 'Medium'),
        ('LARGE', 'Large'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=100, blank=True)
    pet_type = models.CharField(max_length=20, choices=PET_TYPE_CHOICES)
    breed = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=100)
    size = models.CharField(max_length=20, choices=PET_SIZE_CHOICES, default='MEDIUM')
    age_approximate = models.CharField(max_length=50, blank=True)
    
    # Physical Characteristics
    distinctive_marks = models.TextField(blank=True, help_text="Any distinctive marks or features")
    
    # Status and Location
    status = models.CharField(max_length=20, choices=PET_STATUS_CHOICES)
    location_found = models.CharField(max_length=255, help_text="Location where pet was found/lost")
    date_found = models.DateField(help_text="Date when pet was found/lost")
    
    # Contact Information
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_pets')
    contact_phone = models.CharField(max_length=15)
    contact_email = models.EmailField()
    
    # Media
    photo = models.ImageField(upload_to='pet_photos/', blank=True, null=True)
    
    # Additional Information
    additional_info = models.TextField(blank=True, help_text="Any additional information")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Admin verification
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_pets')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        pet_name = self.name if self.name else "Unnamed"
        return f"{pet_name} - {self.get_pet_type_display()} ({self.get_status_display()})"


class Request(models.Model):
    """Model for pet reunion requests"""
    REQUEST_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('REJECTED', 'Rejected'),
    ]
    
    REQUEST_TYPE_CHOICES = [
        ('FOUND_PET', 'I Found a Pet'),
        ('LOST_PET', 'I Lost My Pet'),
        ('ADOPTION', 'Pet Adoption Inquiry'),
    ]
    
    # Request Details
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE_CHOICES)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='requests', null=True, blank=True)
    
    # User Information
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    
    # Request Content
    subject = models.CharField(max_length=200)
    description = models.TextField()
    
    # Status
    status = models.CharField(max_length=20, choices=REQUEST_STATUS_CHOICES, default='PENDING')
    
    # Admin Response
    admin_notes = models.TextField(blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_requests')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_request_type_display()} - {self.requester.username} ({self.get_status_display()})"


class Notification(models.Model):
    """Model for user notifications"""
    NOTIFICATION_TYPE_CHOICES = [
        ('REQUEST_UPDATE', 'Request Update'),
        ('PET_MATCH', 'Potential Pet Match'),
        ('SYSTEM', 'System Notification'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    # Related objects
    related_pet = models.ForeignKey(Pet, on_delete=models.CASCADE, null=True, blank=True)
    related_request = models.ForeignKey(Request, on_delete=models.CASCADE, null=True, blank=True)
    
    # Status
    is_read = models.BooleanField(default=False)
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"


class Comment(models.Model):
    """Model for comments on pet reports"""
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.pet}"
