# Generated by Django 4.1.4 on 2023-06-24 06:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business_admin', '0022_customtoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business_info',
            name='token',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='business_admin.customtoken'),
        ),
    ]
