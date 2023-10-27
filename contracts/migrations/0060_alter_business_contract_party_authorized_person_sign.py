# Generated by Django 3.2.19 on 2023-08-11 18:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contracts', '0059_auto_20230811_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business_contract_party',
            name='authorized_person_sign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='authorized_person_sign', to=settings.AUTH_USER_MODEL),
        ),
    ]