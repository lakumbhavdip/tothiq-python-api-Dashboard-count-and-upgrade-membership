# Generated by Django 4.1.4 on 2023-05-19 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0037_alter_contract_party_contract'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract_party',
            name='contract',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contracts.contracts'),
        ),
    ]
