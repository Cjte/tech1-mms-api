from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from django.core.exceptions import ValidationError
from django.db import transaction
import tempfile
import os

from .models import JobCard, JobStatusLog
from .serializers import JobCardSerializer
from .services import JobCardImportService
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsTechnician, IsAdmin
from .serializers import JobStatusChangeSerializer


class JobCardViewSet(ModelViewSet):
    queryset = JobCard.objects.all()
    serializer_class = JobCardSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def get_permissions(self):
        """Dynamic permission handling based on action"""
        if self.action in ["create", "import_excel"]:
            permission_classes = [IsAdmin]
        elif self.action in ["list", "retrieve"]:
            permission_classes = [IsAdmin | IsTechnician]
        else:
            permission_classes = [IsAdmin]

        return [p() for p in permission_classes]

    def perform_create(self, serializer):
        """Override create to log initial status"""
        with transaction.atomic():
            job = serializer.save()
            # Log the initial status
            JobStatusLog.objects.create(
                job_card=job,
                status=job.status,
                performed_by=self.request.user,
                note="Initial status on creation"
            )

    def perform_update(self, serializer):
        """
        Override update to properly handle:
        - Status transitions (using transition_status)
        - Assignment changes
        """
        with transaction.atomic():
            job = serializer.instance
            previous_status = job.status
            previous_assigned_to = job.assigned_to

            # Check what is being updated
            new_status = serializer.validated_data.get("status", previous_status)
            new_assigned_to = serializer.validated_data.get("assigned_to", previous_assigned_to)

            # Save other fields first (except status if it changed)
            if new_status == previous_status:
                job = serializer.save()
            else:
                # Save non-status fields first
                serializer.save(status=previous_status)
                
                # Use proper transition method
                job.transition_status(new_status, performed_by=self.request.user)

            # Handle assignment change logging
            if previous_assigned_to != new_assigned_to:
                JobStatusLog.objects.create(
                    job_card=job,
                    previous_status=job.status,
                    new_status=job.status,
                    performed_by=self.request.user,
                    note=f"Assigned changed from {previous_assigned_to} to {new_assigned_to}"
                )

    @action(detail=True, methods=["post"], serializer_class=JobStatusChangeSerializer)
    def change_status(self, request, pk=None):
        job = self.get_object()

        serializer = JobStatusChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_status = serializer.validated_data["status"]

        try:
            job.transition_status(new_status, performed_by=request.user)
        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"message": f"Status changed to {new_status} successfully."},
            status=status.HTTP_200_OK
        )



    @action(detail=False, methods=["post"])
    def import_excel(self, request):
        """Import JobCards from uploaded Excel and track initial status"""
        excel_file = request.FILES.get("file")
        if not excel_file:
            return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            for chunk in excel_file.chunks():
                tmp.write(chunk)
            tmp_file = tmp.name

        try:
            # Import and track jobs with performed_by as the current user
            result = JobCardImportService.import_from_excel(tmp_file, performed_by=request.user)
        finally:
            # Clean up temp file
            os.remove(tmp_file)

        return Response(result, status=status.HTTP_200_OK)
