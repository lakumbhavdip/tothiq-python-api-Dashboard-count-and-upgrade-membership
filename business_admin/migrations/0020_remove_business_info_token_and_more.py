# Generated by Django 4.1.4 on 2023-06-24 05:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business_admin', '0019_business_info_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='business_info',
            name='token',
        ),
        migrations.DeleteModel(
            name='business_admin_token',
        ),
    ]
