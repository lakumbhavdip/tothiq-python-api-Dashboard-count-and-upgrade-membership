# Generated by Django 4.1.4 on 2023-05-17 04:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_alter_users_apartment_number_alter_users_area_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='civil_id',
            field=models.CharField(max_length=12, unique=True, validators=[django.core.validators.MinLengthValidator(12)]),
        ),
        migrations.AlterField(
            model_name='users',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
    ]