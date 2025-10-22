from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Pet(models.Model):
    """Model for pets that are found or lost"""
    PET_TYPES = (
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('rabbit', 'Rabbit'),
        ('other', 'Other'),
    )
    
    PET_SIZES = (
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    )
    
    STATUS_CHOICES = (
        ('found', 'Found Pet'),
        ('lost', 'Lost Pet'),
        ('reunited', 'Reunited'),
        ('adopted', 'Adopted'),
    )
    
    # Basic Information
    name = models.CharField(max_length=100, blank=True, help_text="Pet's name if known")
    pet_type = models.CharField(max_length=10, choices=PET_TYPES)
    breed = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=100)
    size = models.CharField(max_length=10, choices=PET_SIZES)
    age_estimate = models.CharField(max_length=50, blank=True, help_text="e.g., 'Young', '2-3 years', 'Senior'")
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('unknown', 'Unknown')], default='unknown')
    
    # Physical Description
    description = models.TextField(help_text="Detailed description of the pet's appearance and behavior")
    distinctive_features = models.TextField(blank=True, help_text="Scars, markings, collar details, etc.")
    
    # Location and Status
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    found_location = models.CharField(max_length=200, help_text="Where the pet was found/lost")
    found_date = models.DateField(help_text="When the pet was found/lost")
    current_location = models.CharField(max_length=200, blank=True, help_text="Current location of the pet")
    
    # Contact Information
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_pets')
    contact_phone = models.CharField(max_length=17)
    contact_email = models.EmailField()
    
    # Administrative
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        name_part = self.name if self.name else "Unnamed"
        return f"{name_part} - {self.get_pet_type_display()} ({self.get_status_display()})"

class PetImage(models.Model):
    """Model for pet images"""
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='pet_images/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.pet}"

class PetRequest(models.Model):
    """Model for managing pet rescue requests and inquiries"""
    REQUEST_TYPES = (
        ('found_report', 'Found Pet Report'),
        ('lost_inquiry', 'Lost Pet Inquiry'),
        ('adoption_request', 'Adoption Request'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )
    
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPES)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='requests', null=True, blank=True)
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pet_requests')
    
    # Request Details
    message = models.TextField(help_text="Additional details about the request")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    # Administrative
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_requests')
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_request_type_display()} by {self.requester.username}"
