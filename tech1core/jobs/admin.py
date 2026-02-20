from django.contrib import admin
from .models import JobCard, JobStatusLog


@admin.register(JobCard)
class JobCardAdmin(admin.ModelAdmin):
    list_display = ("job_card_number", "title", "status", "assigned_to", "created_at")
    list_filter = ("status", "job_type")
    search_fields = ("job_card_number", "title")
    ordering = ("-created_at",)


@admin.register(JobStatusLog)
class JobStatusLogAdmin(admin.ModelAdmin):
    list_display = ("job_card", "previous_status", "new_status", "performed_by", "timestamp")
    list_filter = ("new_status",)
    ordering = ("-timestamp",)
