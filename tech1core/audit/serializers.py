from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    performed_by = serializers.StringRelatedField()
    model_name = serializers.SerializerMethodField()
    object_id = serializers.UUIDField()

    class Meta:
        model = AuditLog
        fields = ['id', 'model_name', 'object_id', 'action', 'performed_by', 'created_at', 'updated_at']

    @extend_schema_field(serializers.CharField())
    def get_model_name(self, obj):
        return obj.content_type.model  # e.g., 'jobcard' or 'jobhandover'
