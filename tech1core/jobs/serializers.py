from rest_framework import serializers
from .models import JobCard

class JobCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobCard
        fields = "__all__"
        read_only_fields = ("status",)



class JobStatusChangeSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=JobCard.STATUS_CHOICES)
