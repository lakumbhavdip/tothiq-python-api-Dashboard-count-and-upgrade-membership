# Generated by Django 4.1.4 on 2023-06-23 06:46

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('business_admin', '0015_delete_business_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='business_admin_token',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('business_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_admin.business_info')),
            ],
            options={
                'db_table': 'business_admin_token',
            },
        ),
    ]