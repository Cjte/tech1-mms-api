from django.db import models
from django.conf import settings
from core.models import BaseModel
from jobs.models import JobCard

class JobExecution(BaseModel):
    STATUS_DRAFT = "DRAFT"
    STATUS_SUBMITTED = "SUBMITTED"

    STATUS_CHOICE = [
        (STATUS_DRAFT, "DRAFT"),
        (STATUS_SUBMITTED, "Submitted")
    ]

    job_card = models.ForeignKey(JobCard, on_delete=models.CASCADE, related_name="executions")
    technician = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    execution_notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default= STATUS_DRAFT)

    def submit(self):
        if self.status == self.STATUS_SUBMITTED:
            raise ValueError("execution already submitted")
        
        if self.job_card.status not in [JobCard.STATUS_IN_PROGRESS, JobCard.STATUS_ASSIGNED]:
            raise ValueError("JobCard cannot be executed in its current status")
        
        self.status = self.STATUS_SUBMITTED
        self.save()

        self.job_card.transition_status(JobCard.STATUS_COMPLETED)


