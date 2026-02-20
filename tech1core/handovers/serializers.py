from rest_framework import serializers
from django.contrib.auth import get_user_model
from jobs.models import JobCard
from .models import JobHandover

User = get_user_model()


class JobHandoverSerializer(serializers.ModelSerializer):
    job_card_id = serializers.UUIDField(write_only=True)

    from_technician = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False
    )
    to_technician = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    from_technician_display = serializers.StringRelatedField(
        source="from_technician",
        read_only=True
    )
    to_technician_display = serializers.StringRelatedField(
        source="to_technician",
        read_only=True
    )

    class Meta:
        model = JobHandover
        fields = [
            "id",
            "job_card_id",
            "from_technician",
            "to_technician",
            "reason",
            "from_technician_display",
            "to_technician_display",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        job_card_id = validated_data.pop("job_card_id")
        job_card = JobCard.objects.get(id=job_card_id)

        request_user = self.context["request"].user
        from_tech = validated_data.get("from_technician", request_user)
        to_tech = validated_data["to_technician"]
        reason = validated_data["reason"]

        handover = JobHandover.create_handover(
            job_card=job_card,
            from_tech=from_tech,
            to_tech=to_tech,
            reason=reason,
        )

        from audit.services import AuditService
        AuditService.log_action(
            user=request_user,
            obj=handover,
            action="Job Handover Created",
        )

        return handover
