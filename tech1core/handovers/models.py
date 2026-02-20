from django.db import models, transaction
from django.conf import settings
from core.models import BaseModel
from jobs.models import JobCard


class JobHandover(BaseModel):
    job_card =models.ForeignKey(JobCard, on_delete=models.CASCADE, related_name="handovers")
    from_technician = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="handover_from")
    to_technician = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="handover_to")
    reason = models.TextField()


    @classmethod
    def create_handover(cls, job_card, from_tech, to_tech, reason):
        if job_card.status not in [JobCard.STATUS_ASSIGNED, JobCard.STATUS_IN_PROGRESS]:
            raise ValueError("handover can only be done on assigned on rin-progress jobs.")
        
        with transaction.atomic():
            job_card.assigned_to = to_tech
            job_card.transition_status(JobCard.STATUS_HANDOVER)
            job_card.save()

            handover = cls.objects.create(
                job_card=job_card,
                from_technician =from_tech,
                to_technician = to_tech,
                reason =reason
            )
        return handover