# Generated by Django 4.1.4 on 2023-06-01 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0027_alter_users_image'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='user_notification',
            table='notification_setting',
        ),
    ]
