# Generated by Django 5.2.3 on 2025-06-19 21:16

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_uservessel_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='guest',
            name='guest_token',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
