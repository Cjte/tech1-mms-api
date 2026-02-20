from celery.schedules import crontab
from celery import app
from .tasks import calculate_kpis_task

app.conf.beat_schedule = {
    "calculate-kpis-everyday": {
        "task": "apps.kpi.tasks.calculate_kpis_task",
        "schedule": crontab(hour=0, minute=0),  # daily at midnight UTC
    }
}
