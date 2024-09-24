from rest_framework import serializers

from logs.models import NginxLog


class NginxLogSerializer(serializers.ModelSerializer):
    """Сериализатор модели NginxLog."""

    class Meta:
        model = NginxLog
        fields = (
            'ip_adress', 'log_date', 'http_method',
            'url', 'response_code', 'response_size'
        )
