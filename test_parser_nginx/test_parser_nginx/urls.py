from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from logs.views import NginxLogViewSet

router = DefaultRouter()
router.register('nginx-logs', NginxLogViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title='Nginx log API',
        default_version='v1',
        description='API для работы с Nginx логами',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

urlpatterns = [
    path('admin', admin.site.urls),
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui(
        'swagger', cache_timeout=0), name='schema-swager'
    ),
    path('logs/', include('logs.urls')),
]
