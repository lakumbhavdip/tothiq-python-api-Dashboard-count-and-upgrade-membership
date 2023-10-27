# Generated by Django 3.2.19 on 2023-08-23 15:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contracts', '0067_auto_20230823_1525'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='business_contract_party',
            name='authorized_person_sign',
        ),
        migrations.AddField(
            model_name='business_contract_party',
            name='authorized_person_sign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='authorized_person_sign', to=settings.AUTH_USER_MODEL),
        ),
    ]
