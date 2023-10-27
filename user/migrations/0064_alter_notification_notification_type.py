# Generated by Django 3.2.19 on 2023-09-20 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0063_alter_users_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('new_comment', 'Get notification for new comments.'), ('status_change', 'Get notification for status changes.'), ('membership_expiration', 'Get notification for membership expriration.'), ('user_addition', 'Get notification for users add on.'), ('contract_deletion', 'Get Notification on deleting contract.'), ('contract_review', 'Get notification on reviewed contract.'), ('contract_signature', 'Get notification on signature.'), ('contract_cancellation', 'Get notification on cancted contract.'), ('new_draft_contract', 'Get notification on new or draft contract.')], default='', max_length=100, null=True),
        ),
    ]
