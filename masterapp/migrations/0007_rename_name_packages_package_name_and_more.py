# Generated by Django 4.1.4 on 2023-05-12 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterapp', '0006_rename_address_type_packages_alter_packages_table'),
    ]

    operations = [
        migrations.RenameField(
            model_name='packages',
            old_name='name',
            new_name='package_name',
        ),
        migrations.AddField(
            model_name='packages',
            name='description',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='packages',
            name='price',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='packages',
            name='validity_days',
            field=models.CharField(default='', max_length=50),
        ),
    ]
