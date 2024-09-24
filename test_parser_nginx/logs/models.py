from django.db import models


class NginxLog(models.Model):
    """Модель для хранения данных лога."""

    ip_adress = models.GenericIPAddressField()
    log_date = models.DateTimeField()
    http_method = models.CharField(max_length=10)
    url = models.CharField(max_length=2000)
    response_code = models.IntegerField()
    response_size = models.IntegerField()

    def __str__(self):
        return f'{self.ip_adress} - {self.http_method} {self.url}'
