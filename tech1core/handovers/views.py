from rest_framework import generics, permissions
from .models import JobHandover
from .serializers import JobHandoverSerializer

class JobHandoverListCreateView(generics.ListCreateAPIView):
    """
    List all job handovers or create a new handover.
    """
    queryset = JobHandover.objects.all().select_related('job_card', 'from_technician', 'to_technician')
    serializer_class = JobHandoverSerializer
    permission_classes = [permissions.IsAuthenticated]
