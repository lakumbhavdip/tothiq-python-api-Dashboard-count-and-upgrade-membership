# Generated by Django 4.1.4 on 2023-05-17 08:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_users_status_users_verified_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='varified_at',
        ),
    ]
