# Generated by Django 3.2.19 on 2023-09-01 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('masterapp', '0055_membership_number_of_templates'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contract_histroy',
            name='user',
        ),
    ]
