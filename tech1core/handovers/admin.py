from django.contrib import admin
from .models import JobHandover

@admin.register(JobHandover)
class HandoverAdmin(admin.ModelAdmin):
    list_display = ('job_card', 'from_technician', 'to_technician')
    ordering = ("-created_at",)
