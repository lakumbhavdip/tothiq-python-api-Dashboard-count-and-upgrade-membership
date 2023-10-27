# Generated by Django 4.1.4 on 2023-06-15 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0035_users_account_type_alter_users_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='account_type',
            field=models.CharField(choices=[('individual', 'Individual'), ('business', 'Business')], max_length=255, null=True),
        ),
    ]