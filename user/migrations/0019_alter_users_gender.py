# Generated by Django 4.1.4 on 2023-05-18 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_remove_users_varified_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=6),
        ),
    ]