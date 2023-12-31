# Generated by Django 4.1.4 on 2023-06-29 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0052_contract_party_first_party_civil_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract_party',
            name='contract',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contract_parties', to='contracts.contracts'),
        ),
    ]
