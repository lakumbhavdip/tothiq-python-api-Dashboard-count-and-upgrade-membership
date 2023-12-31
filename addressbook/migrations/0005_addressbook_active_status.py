# Generated by Django 4.1.4 on 2023-07-07 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addressbook', '0004_addressbook_created_at_addressbook_deleted_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='addressbook',
            name='active_status',
            field=models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('blocked', 'Blocked'), ('deleted', 'Deleted')], max_length=100, null=True),
        ),
    ]
