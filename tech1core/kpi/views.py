from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.cache import cache
from drf_spectacular.utils import extend_schema
from .services import KIPService
from .serializers import KPISerializer

@extend_schema(
    responses=KPISerializer(many=True)  # tells Swagger the response is a list of KPI objects
)
class DashboardKPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve the current KPIs, using cache if available.
        """
        kpis = cache.get("dashboard_kpis")
        if not kpis:
            kpis = KIPService.calculate_kips()
            cache.set("dashboard_kpis", kpis, timeout=3600)
        serializer = KPISerializer(kpis, many=True)
        return Response({"kpis": serializer.data})
