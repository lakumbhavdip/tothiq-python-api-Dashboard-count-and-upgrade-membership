# Generated by Django 4.1.4 on 2023-06-16 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0038_notification_pin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='pin',
            field=models.BooleanField(default=False),
        ),
    ]
