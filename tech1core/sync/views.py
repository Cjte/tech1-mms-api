from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from sync.serializers import OfflineSyncSerializer
from jobs.models import JobCard
from execution.models import JobExecution
from handovers.models import JobHandover


class OfflineSyncView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OfflineSyncSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        jobs_data = serializer.validated_data["jobs"]
        results = []

        with transaction.atomic():
            for job_data in jobs_data:
                job_id = job_data["id"]

                try:
                    job = JobCard.objects.get(id=job_id)

                    # Update job fields
                    if "status" in job_data:
                        job.status = job_data["status"]

                    if "assigned_to" in job_data:
                        job.assigned_to_id = job_data["assigned_to"]

                    job.save()

                    # Sync executions
                    for exec_data in job_data.get("executions", []):
                        execution = JobExecution.objects.filter(
                            id=exec_data.get("id")
                        ).first()

                        if execution:
                            if "execution_notes" in exec_data:
                                execution.execution_notes = exec_data["execution_notes"]

                            if exec_data.get("status") == JobExecution.STATUS_SUBMITTED:
                                execution.submit()
                            else:
                                execution.save()
                        else:
                            JobExecution.objects.create(
                                job_card=job,
                                technician=request.user,
                                execution_notes=exec_data.get("execution_notes", ""),
                                status=exec_data.get(
                                    "status",
                                    JobExecution.STATUS_DRAFT
                                )
                            )

                    # Sync handovers
                    for handover_data in job_data.get("handovers", []):
                        JobHandover.create_handover(
                            job_card=job,
                            from_tech=request.user,
                            to_tech_id=handover_data["to_technician"],
                            reason=handover_data.get("reason", "")
                        )

                    results.append({
                        "job_id": str(job_id),
                        "status": "synced"
                    })

                except Exception as e:
                    results.append({
                        "job_id": str(job_id),
                        "status": "error",
                        "message": str(e)
                    })

        return Response({"results": results})
