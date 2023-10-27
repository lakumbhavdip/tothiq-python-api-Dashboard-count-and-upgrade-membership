# Generated by Django 4.1.4 on 2023-05-15 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_alter_users_area_alter_users_block_alter_users_floor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='apartment_number',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='users',
            name='area',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='users',
            name='block',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='users',
            name='floor',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='users',
            name='house_number',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='users',
            name='street_name_number',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
