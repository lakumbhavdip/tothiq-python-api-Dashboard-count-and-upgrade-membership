# Generated by Django 4.1.4 on 2023-07-21 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0056_alter_contracts_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='contracts',
            name='pin',
            field=models.BooleanField(default=False),
        ),
    ]
