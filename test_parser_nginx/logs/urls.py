from rest_framework.routers import DefaultRouter

from logs.views import NginxLogViewSet

router = DefaultRouter()
router.register('nginx-logs', NginxLogViewSet)

urlpatterns = router.urls
