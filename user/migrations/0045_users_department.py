# Generated by Django 4.1.4 on 2023-06-24 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business_admin', '0028_alter_business_department_business'),
        ('user', '0044_users_business'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='business_admin.business_department'),
        ),
    ]
