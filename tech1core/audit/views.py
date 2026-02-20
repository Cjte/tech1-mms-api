# audit/views.py
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django.contrib.contenttypes.models import ContentType
from .models import AuditLog
from .serializers import AuditLogSerializer

class AuditLogView(generics.ListAPIView):
    """
    List all audit logs.
    Supports filtering by performed_by ID, model name, and action.
    """
    queryset = AuditLog.objects.all().select_related('performed_by', 'content_type')
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['action', 'performed_by__username']  # cannot search GenericForeignKey directly
    ordering_fields = ['timestamp', 'performed_by__username']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Optionally filter by performed_by or model_name via query parameters:
        ?user_id=1&model_name=jobcard
        """
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        model_name = self.request.query_params.get('model_name')

        if user_id:
            queryset = queryset.filter(performed_by_id=user_id)
        if model_name:
            # Filter using content_type__model (lowercase by default)
            queryset = queryset.filter(content_type__model=model_name.lower())

        return queryset
