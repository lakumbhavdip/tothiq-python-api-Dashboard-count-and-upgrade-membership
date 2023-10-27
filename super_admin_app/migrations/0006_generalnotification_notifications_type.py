# Generated by Django 3.2.19 on 2023-09-04 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('super_admin_app', '0005_auto_20230824_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalnotification',
            name='notifications_type',
            field=models.CharField(choices=[('both', 'Both'), ('email', 'Email'), ('push-notification', 'Push Notification')], default='both', max_length=20),
        ),
    ]