# Generated by Django 4.1.4 on 2023-05-15 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_alter_users_address_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='area',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='block',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='floor',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='house_number',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='street_name_number',
            field=models.CharField(default='', max_length=200, null=True),
        ),
    ]
