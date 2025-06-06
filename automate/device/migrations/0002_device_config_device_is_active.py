# Generated by Django 5.2 on 2025-04-30 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='config',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='device',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
