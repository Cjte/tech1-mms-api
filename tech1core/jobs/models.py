from django.db import models, transaction
from core.models import BaseModel
from django.conf import settings
from django.core.exceptions import ValidationError
from audit.services import AuditService

class JobCard(BaseModel):
    STATUS_OPEN = "OPEN"
    STATUS_ASSIGNED = "ASSIGNED"
    STATUS_IN_PROGRESS = "IN_PROGRESS"
    STATUS_HANDOVER = "HANDOVER"
    STATUS_COMPLETED = "COMPLETED"
    STATUS_CLOSED = "CLOSED"

    STATUS_CHOICES = (
        (STATUS_OPEN, "Open"),
        (STATUS_ASSIGNED, "Assigned"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_HANDOVER, "Handover"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CLOSED, "Closed"),
    )

    TYPE_CHOICES = [
        ("Corrective", "Corrective"),
        ("Preventive", "Preventive"),
        ("Breakdown", "Breakdown"),
    ]

    job_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        null=True,
        blank=True
    )
    job_card_number = models.CharField(
    max_length=100,
    unique=True,
    null=True,
    blank=True
)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_jobs"
    )

    def transition_status(self, new_status, performed_by=None):
        """
        Transition status with validation and logging.
        """
        allowed = {
            self.STATUS_OPEN: [self.STATUS_ASSIGNED],
            self.STATUS_ASSIGNED: [self.STATUS_IN_PROGRESS, self.STATUS_HANDOVER],
            self.STATUS_IN_PROGRESS: [self.STATUS_HANDOVER, self.STATUS_COMPLETED],
            self.STATUS_HANDOVER: [self.STATUS_IN_PROGRESS],
            self.STATUS_COMPLETED: [self.STATUS_CLOSED],
            self.STATUS_CLOSED: []
        }

        if new_status not in allowed[self.status]:
            raise ValidationError(
                f"Invalid status transition from {self.status} to {new_status}"
            )

        old_status = self.status
        with transaction.atomic():
            self.status = new_status
            self.save()

            # Create a log entry
            JobStatusLog.objects.create(
                job_card=self,
                previous_status=old_status,
                new_status=new_status,
                performed_by=performed_by
            )


        AuditService.log_action(
        user=performed_by,
        obj=self,
        action="status_changed",
        description=f"Status changed from {old_status} to {new_status}"
    )



class JobStatusLog(BaseModel):
    job_card = models.ForeignKey(JobCard, on_delete=models.CASCADE, related_name="status_logs")
    previous_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
