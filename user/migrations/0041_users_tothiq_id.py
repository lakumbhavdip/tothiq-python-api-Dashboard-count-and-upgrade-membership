# Generated by Django 4.1.4 on 2023-06-19 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0040_alter_users_active_status_alter_users_address_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='tothiq_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
