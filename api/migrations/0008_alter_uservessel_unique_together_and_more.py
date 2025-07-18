# Generated by Django 5.2.3 on 2025-06-20 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_remove_task_order_remove_task_description_task_guest_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='uservessel',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='uservessel',
            constraint=models.UniqueConstraint(fields=('user', 'vessel'), name='unique_user_per_vessel'),
        ),
        migrations.AddConstraint(
            model_name='uservessel',
            constraint=models.UniqueConstraint(condition=models.Q(('is_primary', True)), fields=('vessel',), name='only_one_primary_per_vessel'),
        ),
    ]
