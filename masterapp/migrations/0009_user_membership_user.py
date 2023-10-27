# Generated by Django 4.1.4 on 2023-05-12 09:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('masterapp', '0008_alter_packages_package_name_user_membership'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_membership',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
