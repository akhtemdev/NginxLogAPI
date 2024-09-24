from datetime import datetime
import json
import tempfile

from django.core.management.base import BaseCommand
from django.db import transaction
import requests

from logs.models import NginxLog


class Command(BaseCommand):
    """Парсер логов nginx."""

    def add_arguments(self, parser):
        parser.add_argument(
            'file_url', type=str, help='URL файла логов с Google Drive'
        )

    def handle(self, *args, **options):
        file_url = options['file_url']

        if 'drive.google.com' in file_url:
            file_id = self._extract_file_id(file_url)
            temp_file_path = self._download_file_from_google_drive(file_id)
        else:
            self.stderr.write(self.style.ERROR(
                'Некорректная ссылка. Только Google Drive.'
                )
            )
            return

        batch_size = 1000
        logs_to_insert = []

        with open(temp_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line:
                    log = json.loads(line.strip())
                    log_date = datetime.strptime(
                        log['time'], '%d/%b/%Y:%H:%M:%S %z'
                    )
                    method, url, _ = log['request'].split(' ')

                    logs_to_insert.append(
                        NginxLog(
                            ip_adress=log['remote_ip'],
                            log_date=log_date,
                            http_method=method,
                            url=url,
                            response_code=int(log['response']),
                            response_size=int(log['bytes']),
                        )
                    )

                if len(logs_to_insert) >= batch_size:
                    self._bulk_insert(logs_to_insert)
                    logs_to_insert = []

            if logs_to_insert:
                self._bulk_insert(logs_to_insert)

        self.stdout.write(self.style.SUCCESS('Файл логов спарсен и сохранён в БД!'))

    @transaction.atomic
    def _bulk_insert(self, logs):
        NginxLog.objects.bulk_create(logs)

    def _extract_file_id(self, file_url):
        """Извлекает file_id из ссылки Google Drive."""
        file_id = file_url.split('/d/')[1].split('/view')[0]
        return file_id

    def _download_file_from_link(self, file_id):
        """Загружает файл с Google Drive и сохраняет его."""
        URL = "https://drive.google.com/uc?export=download"
        session = requests.Session()

        response = session.get(URL, params={'id': file_id}, stream=True)
        response.raise_for_status()

        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".json"
        ) as temp_file:
            for chunk in response.iter_content(1024):
                if chunk:
                    temp_file.write(chunk)
            temp_file_path = temp_file.name

        self.stdout.write(self.style.SUCCESS(
            f'Файл загружен и сохранён как {temp_file_path}')
        )

        return temp_file_path
