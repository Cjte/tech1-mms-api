from celery import shared_task
from django.core.cache import cache
from .services import KIPService

@shared_task
def calculate_kpis_task():
    """
    Calculate KPIs using KIPService and store in cache for fast retrieval.
    """
    kpis = KIPService.calculate_kips()
    cache.set("dashboard_kpis", kpis, timeout=3600)  # cache for 1 hour
    return kpis
