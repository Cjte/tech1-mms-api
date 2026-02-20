from rest_framework import serializers
from jobs.models import JobCard
from execution.models import JobExecution
from handovers.models import JobHandover


class JobExecutionSyncSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)
    execution_notes = serializers.CharField(required=False, allow_blank=True)
    status = serializers.CharField(required=False)


class JobHandoverSyncSerializer(serializers.Serializer):
    to_technician = serializers.UUIDField()
    reason = serializers.CharField(required=False, allow_blank=True)


class JobCardSyncSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    status = serializers.CharField(required=False)
    assigned_to = serializers.UUIDField(required=False)

    executions = JobExecutionSyncSerializer(many=True, required=False)
    handovers = JobHandoverSyncSerializer(many=True, required=False)


class OfflineSyncSerializer(serializers.Serializer):
    jobs = JobCardSyncSerializer(many=True)
