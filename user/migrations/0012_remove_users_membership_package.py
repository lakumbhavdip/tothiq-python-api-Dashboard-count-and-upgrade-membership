# Generated by Django 4.1.4 on 2023-05-13 09:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_users_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='membership_package',
        ),
    ]