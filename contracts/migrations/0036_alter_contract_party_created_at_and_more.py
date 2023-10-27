# Generated by Django 4.1.4 on 2023-05-19 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0035_alter_contract_party_civil_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract_party',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='contract_party',
            name='party_type',
            field=models.CharField(choices=[('first', 'First'), ('second', 'Second')], max_length=10),
        ),
        migrations.AlterField(
            model_name='contract_party',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]