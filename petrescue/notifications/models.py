from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    """Model for user notifications"""
    NOTIFICATION_TYPES = (
        ('pet_match', 'Potential Pet Match'),
        ('request_update', 'Request Status Update'),
        ('new_pet_report', 'New Pet Report'),
        ('system_message', 'System Message'),
    )
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    # Optional links
    related_pet_id = models.IntegerField(null=True, blank=True)
    related_request_id = models.IntegerField(null=True, blank=True)
    action_url = models.URLField(blank=True)
    
    # Status
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.title}"

class PetMatch(models.Model):
    """Model for tracking potential matches between found and lost pets"""
    found_pet = models.ForeignKey('pets.Pet', on_delete=models.CASCADE, related_name='found_matches')
    lost_pet = models.ForeignKey('pets.Pet', on_delete=models.CASCADE, related_name='lost_matches')
    
    # Match scoring
    similarity_score = models.FloatField(help_text="Calculated similarity score between pets")
    match_factors = models.JSONField(help_text="Factors that contributed to the match")
    
    # Status
    is_confirmed = models.BooleanField(default=False)
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['found_pet', 'lost_pet']
        ordering = ['-similarity_score', '-created_at']
    
    def __str__(self):
        return f"Match: {self.found_pet} <-> {self.lost_pet} (Score: {self.similarity_score})"
