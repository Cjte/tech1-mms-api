from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import JobExecution
from .serializers import JobExecutionSerializer


class JobExecutionViewSet(ModelViewSet):
    queryset = JobExecution.objects.all()
    serializer_class = JobExecutionSerializer
    permission_classes = [IsAuthenticated]



    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        execution = self.get_object()
        try:
            execution.submit()

        except ValueError as e:
            return Response({"error": str(e)}, status=400)
        return Response({"status": "submitted"})


