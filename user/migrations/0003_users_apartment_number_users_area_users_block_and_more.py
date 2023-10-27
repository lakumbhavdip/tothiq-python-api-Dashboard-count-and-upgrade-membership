# Generated by Django 4.1.4 on 2023-05-11 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_users_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='apartment_number',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='users',
            name='area',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='users',
            name='block',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='users',
            name='floor',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='users',
            name='house_number',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='users',
            name='street_name_number',
            field=models.CharField(default='', max_length=200),
        ),
    ]