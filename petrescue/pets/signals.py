from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import PetReport, ReportStatus


def _send_email(subject: str, message: str, recipient_list: list[str]) -> None:
    if not recipient_list:
        return
    send_mail(
        subject=subject,
        message=message,
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
        recipient_list=recipient_list,
        fail_silently=True,
    )


@receiver(post_save, sender=PetReport)
def notify_report_status(sender, instance: PetReport, created: bool, **kwargs):
    if created:
        _send_email(
            subject=f"PetRescue report created: {instance.reference_code}",
            message=(
                f"Hi {instance.reporter_name},\n\n"
                f"Your {instance.get_report_type_display()} report was created with reference code "
                f"{instance.reference_code}. We'll notify you of updates.\n\n"
                f"- PetRescue"
            ),
            recipient_list=[instance.reporter_email],
        )
        return

    # On updates to status, notify reporter
    if "status" in instance.get_deferred_fields():
        # Not reliable here; instead, always send when saved and status changed would require tracking previous.
        pass

    # Simple approach: if status is resolved or matched, notify
    if instance.status in {ReportStatus.MATCHED, ReportStatus.RESOLVED}:
        _send_email(
            subject=f"Update on your pet report {instance.reference_code}",
            message=(
                f"Hi {instance.reporter_name},\n\n"
                f"Your report status is now '{instance.get_status_display()}'.\n\n"
                f"You can view details at: {instance.get_absolute_url()}\n\n"
                f"- PetRescue"
            ),
            recipient_list=[instance.reporter_email],
        )
