# Generated by Django 4.1.4 on 2023-08-01 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_admin', '0039_rename_parent_id_business_department_parent_department_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business_info',
            name='authorized_signatory_expiry_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='business_info',
            name='licence_expiry_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]