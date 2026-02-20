from django.utils import timezone
from datetime import timedelta
from jobs.models import JobCard
from handovers.models import JobHandover

class KIPService:
    @staticmethod
    def calculate_kips():

        now = timezone.now()

        total_jobs = JobCard.objects.count()
        closed_jobs = JobCard.objects.filter(status=JobCard.STATUS_CLOSED).count()
        in_progress_jobs = JobCard.objects.filter(status = JobCard.STATUS_IN_PROGRESS).count()
        assigned_jobs = JobCard.objects.filter(status = JobCard.STATUS_ASSIGNED).count()

        closure_rate = (closed_jobs / total_jobs * 100) if total_jobs > 0 else 0

        completed_jobs = JobCard.objects.filter(status = JobCard.STATUS_CLOSED)
        aging_list = [(job.update_at - job.created_at).total_seconds() for job in completed_jobs]
        avg_aging = (sum(aging_list) / len(aging_list)) / 3600 if aging_list else 0

        backlog = total_jobs - closed_jobs



        overdue_jobs = JobCard.objects.filter(
            status__in  = [JobCard.STATUS_OPEN, JobCard.STATUS_ASSIGNED, JobCard.STATUS_IN_PROGRESS],
            updated_at__lt = now - timedelta(days=2)

        ).count()

        total_handovers = JobHandover.objects.count()
        handover_freq = (total_handovers/ total_jobs *100) if total_jobs > 0 else 0


        return [
    {"metric_name": "Total Jobs", "value": float(total_jobs)},
    {"metric_name": "Closure Rate (%)", "value": float(round(closure_rate, 2))},
    {"metric_name": "Average Aging (Hours)", "value": float(round(avg_aging, 2))},
    {"metric_name": "Backlog", "value": float(backlog)},
    {"metric_name": "Overdue Jobs", "value": float(overdue_jobs)},
    {"metric_name": "Handover Frequency (%)", "value": float(round(handover_freq, 2))},
    {"metric_name": "Assigned Jobs", "value": float(assigned_jobs)},
    {"metric_name": "In Progress Jobs", "value": float(in_progress_jobs)},
]
