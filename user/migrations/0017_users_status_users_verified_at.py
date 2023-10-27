# Generated by Django 4.1.4 on 2023-05-17 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_alter_users_civil_id_alter_users_date_of_birth'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='users',
            name='verified_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
