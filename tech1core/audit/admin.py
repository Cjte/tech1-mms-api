from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("content_type", "object_id", "action", "performed_by", "created_at")
    list_filter = ("content_type", "action")
    search_fields = ("object_id",)
    ordering = ("-created_at",)
