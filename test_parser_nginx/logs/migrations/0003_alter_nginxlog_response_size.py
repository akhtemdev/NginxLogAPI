# Generated by Django 5.1.1 on 2024-09-24 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0002_rename_uri_nginxlog_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nginxlog',
            name='response_size',
            field=models.IntegerField(),
        ),
    ]
