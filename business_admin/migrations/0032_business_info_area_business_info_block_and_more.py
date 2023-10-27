# Generated by Django 4.1.4 on 2023-07-04 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_admin', '0031_alter_business_info_authorized_signatory_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='business_info',
            name='area',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='business_info',
            name='block',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='business_info',
            name='building_name_number',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='business_info',
            name='office_number',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='business_info',
            name='street_name_number',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
