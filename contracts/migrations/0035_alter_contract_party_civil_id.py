# Generated by Django 4.1.4 on 2023-05-19 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0034_alter_contract_party_civil_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract_party',
            name='civil_id',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]