from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from logs.models import NginxLog
from logs.serializers import NginxLogSerializer


class NginxLogViewSet(viewsets.ModelViewSet):
    """ViewSet для NginxLog."""

    queryset = NginxLog.objects.all()
    serializer_class = NginxLogSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['response_code', 'http_method']
    search_fields = ['ip_adress', 'url']
    ordering_fields = ['log_date', 'response_size']
    ordering = ['-log_date']
