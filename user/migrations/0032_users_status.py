# Generated by Django 4.1.4 on 2023-06-02 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0031_remove_users_status_users_active_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
