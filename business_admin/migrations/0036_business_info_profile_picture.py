# Generated by Django 4.1.4 on 2023-07-05 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_admin', '0035_business_info_area_arabic_business_info_block_arabic_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='business_info',
            name='profile_picture',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
