from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Pet(models.Model):
    PET_TYPES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('rabbit', 'Rabbit'),
        ('hamster', 'Hamster'),
        ('other', 'Other'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('unknown', 'Unknown'),
    ]
    
    STATUS_CHOICES = [
        ('found', 'Found'),
        ('lost', 'Lost'),
        ('reunited', 'Reunited'),
        ('adopted', 'Adopted'),
    ]
    
    # Basic pet information
    name = models.CharField(max_length=100, blank=True, null=True)
    pet_type = models.CharField(max_length=20, choices=PET_TYPES)
    breed = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='unknown')
    age = models.PositiveIntegerField(blank=True, null=True)
    size = models.CharField(max_length=20, choices=[
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    ], blank=True, null=True)
    
    # Status and location
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='found')
    location_found = models.CharField(max_length=200)
    date_found = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    
    # Contact information
    finder_name = models.CharField(max_length=100)
    finder_phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )]
    )
    finder_email = models.EmailField()
    
    # Images
    image = models.ImageField(upload_to='pet_images/', blank=True, null=True)
    
    # Admin management
    is_verified = models.BooleanField(default=False)
    admin_notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets_created')
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_found']
    
    def __str__(self):
        return f"{self.pet_type.title()} - {self.location_found} ({self.status})"


class PetRequest(models.Model):
    REQUEST_TYPES = [
        ('claim', 'Claim Pet'),
        ('report_lost', 'Report Lost Pet'),
        ('adopt', 'Adoption Request'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    
    # Request details
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPES)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='requests')
    requester_name = models.CharField(max_length=100)
    requester_phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )]
    )
    requester_email = models.EmailField()
    
    # Request information
    description = models.TextField(help_text="Please provide details about your relationship to this pet or why you want to adopt")
    proof_of_ownership = models.TextField(blank=True, null=True, help_text="Describe any identifying features, microchip info, or other proof")
    
    # Status and admin management
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_requests')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.request_type} for {self.pet} by {self.requester_name}"


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('pet_found', 'Pet Found'),
        ('request_approved', 'Request Approved'),
        ('request_rejected', 'Request Rejected'),
        ('pet_reunited', 'Pet Reunited'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    related_pet = models.ForeignKey(Pet, on_delete=models.CASCADE, null=True, blank=True)
    related_request = models.ForeignKey(PetRequest, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )],
        blank=True, null=True
    )
    address = models.TextField(blank=True, null=True)
    is_volunteer = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"