# Generated by Django 3.2.19 on 2023-09-08 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0057_users_full_name_arabic'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='address_type_arabic',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='area_arabic',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='gender_arabic',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='house_number_arabic',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='street_name_number_arabic',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]
