# Generated by Django 3.2.19 on 2023-09-06 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('masterapp', '0063_remove_country_currency_currency_code'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='country_currency',
            new_name='countrycurrency',
        ),
    ]