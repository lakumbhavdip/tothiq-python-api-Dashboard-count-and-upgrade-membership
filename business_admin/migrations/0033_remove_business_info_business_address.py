# Generated by Django 4.1.4 on 2023-07-04 06:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business_admin', '0032_business_info_area_business_info_block_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='business_info',
            name='business_address',
        ),
    ]
