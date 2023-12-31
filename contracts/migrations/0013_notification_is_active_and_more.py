# Generated by Django 4.1.4 on 2023-05-08 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0012_notification_notification_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('new_comment', 'Get notification for new comments.'), ('status_change', 'Get notification for status changes.'), ('membership_expiration', 'Get notification for membership expriration.'), ('user_addition', 'Get notification for users add on.'), ('contract_deletion', 'Get Notification on deleting contract.'), ('contract_review', 'Get notification on reviewed contract.'), ('contract_signature', 'Get notification on signature.'), ('contract_cancellation', 'Get notification on cancted contract.'), ('new_draft_contract', 'Get notification on new or draft contract.')], default='', max_length=100),
        ),
    ]
