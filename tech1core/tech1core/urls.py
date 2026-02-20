from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from jobs.views import JobCardViewSet
from execution.views import JobExecutionViewSet
from kpi.views import DashboardKPIView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from sync.views import OfflineSyncView
from handovers.views import JobHandoverListCreateView
from audit.views import AuditLogView

from users.views import UserRegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register("jobs", JobCardViewSet)
router.register("executions", JobExecutionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API schema and documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    # API endpoints
    path("api/", include(router.urls)),
    path("api/dashboard-kpis/", DashboardKPIView.as_view(), name="dashboard-kpis"),
    path("api/sync/offline/", OfflineSyncView.as_view(), name="offline_sync"),
    path("api/handover/", JobHandoverListCreateView.as_view(), name="job-handover"),
    path("api/logs/", AuditLogView.as_view(), name='audit-logs'),

    # JWT auth
    path("register/", UserRegisterView.as_view(), name="user-register"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

]
