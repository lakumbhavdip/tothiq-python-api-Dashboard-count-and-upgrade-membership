# Generated by Django 4.1.4 on 2023-06-21 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_admin', '0010_business_users_department_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business_info',
            name='business_contact_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
