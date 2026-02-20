from rest_framework import serializers

class KPISerializer(serializers.Serializer):
    metric_name = serializers.CharField()
    value = serializers.FloatField()
