# Generated by Django 3.2.19 on 2023-08-23 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0068_auto_20230823_1527'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='business_contract_party',
            name='authorized_person_sign',
        ),
        migrations.AddField(
            model_name='business_contract_party',
            name='authorized_person_ids',
            field=models.TextField(null=True),
        ),
    ]