# Generated by Django 4.1.4 on 2023-06-19 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_admin', '0007_alter_business_users_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='business_users',
            name='user_role',
            field=models.CharField(choices=[('individual_user', 'Individual User'), ('business_user', 'Business User'), ('business_admin', 'Business Admin')], max_length=255, null=True),
        ),
    ]
