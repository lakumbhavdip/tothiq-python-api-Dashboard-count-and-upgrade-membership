# Generated by Django 4.1.4 on 2023-06-03 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_admin', '0001_initial'), 
    ]

    operations = [
        migrations.AlterField(
            model_name='business_admin_users',
            name='authorized_signatory_expiry_date',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='business_admin_users',
            name='business_address',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='business_admin_users',
            name='business_contact_number',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='business_admin_users',
            name='business_email_address',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='business_admin_users',
            name='business_name',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='business_admin_users',
            name='extension_number',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='business_admin_users',
            name='licence_expiry_date',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='business_admin_users',
            name='password',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
