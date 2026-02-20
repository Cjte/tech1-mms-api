from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from core.models import BaseModel
from .services import AuditService
from .models import AuditLog  # Import the model to exclude it

@receiver(post_save)
def audit_post_save(sender, instance, created, **kwargs):
    # Only audit BaseModel subclasses, but skip AuditLog itself
    if not issubclass(sender, BaseModel) or issubclass(sender, AuditLog):
        return

    # Get user if available; fallback to None
    user = getattr(instance, 'last_modified_by', None)
    action = 'Created' if created else 'Updated'
    AuditService.log_action(user=user, obj=instance, action=action)

@receiver(post_delete)
def audit_post_delete(sender, instance, **kwargs):
    # Skip if not BaseModel or is AuditLog itself
    if not issubclass(sender, BaseModel) or issubclass(sender, AuditLog):
        return

    user = getattr(instance, 'last_modified_by', None)
    AuditService.log_action(user=user, obj=instance, action='Deleted')
