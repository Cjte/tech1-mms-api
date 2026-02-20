from rest_framework import serializers
from .models import JobExecution

class JobExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model =JobExecution
        fields = "__all__"
        read_only_fields = ("status", "technician")

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["technician"] = user
        return super().create(validated_data)
    