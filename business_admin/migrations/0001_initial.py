# Generated by Django 4.1.4 on 2023-06-03 07:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='business_admin_users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=500)),
                ('email', models.CharField(max_length=500)),
                ('password', models.CharField(max_length=500)),
                ('business_name', models.CharField(max_length=500)),
                ('business_email_address', models.CharField(max_length=500)),
                ('business_contact_number', models.IntegerField()),
                ('extension_number', models.IntegerField()),
                ('business_address', models.CharField(max_length=500)),
                ('licence_expiry_date', models.DateField()),
                ('authorized_signatory_expiry_date', models.DateField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'business_admin_users',
            },
        ),
    ]
