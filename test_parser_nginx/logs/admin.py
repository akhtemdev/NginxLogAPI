from django.contrib import admin

from logs.models import NginxLog


@admin.register(NginxLog)
class NginxLogAdmin(admin.ModelAdmin):
    """Админ панель модели NginxLog."""

    list_display = (
        'ip_adress', 'log_date', 'http_method',
        'url', 'response_code', 'response_size'
    )
    search_fields = ('ip_adress', 'http_method', 'url')
    list_filter = ('response_code', 'http_method', 'log_date')
