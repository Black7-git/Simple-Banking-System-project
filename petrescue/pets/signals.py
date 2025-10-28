from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Claim, PetReport


@receiver(post_save, sender=Claim)
def notify_on_claim_created(sender, instance: Claim, created: bool, **kwargs):
    if not created:
        return
    report = instance.pet
    if report.contact_email:
        subject = "New claim submitted for your found pet report"
        message = (
            f"A new claim has been submitted for your report at {report.location_found} on {report.date_found}.\n\n"
            f"Claimer: {instance.claimer_name} ({instance.claimer_email})\n"
            f"Message: {instance.message}"
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [report.contact_email],
            fail_silently=True,
        )


@receiver(pre_save, sender=Claim)
def notify_on_claim_status_change(sender, instance: Claim, **kwargs):
    if not instance.pk:
        return
    try:
        previous = Claim.objects.get(pk=instance.pk)
    except Claim.DoesNotExist:
        return

    if previous.status != instance.status:
        # Status changed; notify claimer
        subject = "Your claim status has been updated"
        message = (
            f"Your claim for pet report #{instance.pet_id} is now: {instance.get_status_display()}"
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.claimer_email],
            fail_silently=True,
        )
        # If approved, mark report as claimed
        if instance.status == "approved":
            PetReport.objects.filter(pk=instance.pet_id).update(status="claimed")
