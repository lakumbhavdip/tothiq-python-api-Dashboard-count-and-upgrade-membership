# Generated by Django 4.1.4 on 2023-07-19 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0054_users_membership_expiry_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]