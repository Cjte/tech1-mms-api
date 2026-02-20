from .models import AuditLog
from django.contrib.contenttypes.models import ContentType

class AuditService:
    @staticmethod
    def log_action(user, obj, action, description=None):
        AuditLog.objects.create(
            performed_by=user,
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.id,
            action=action
        )
