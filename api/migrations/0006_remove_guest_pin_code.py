# Generated by Django 5.2.3 on 2025-06-19 21:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_guest_guest_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guest',
            name='pin_code',
        ),
    ]
