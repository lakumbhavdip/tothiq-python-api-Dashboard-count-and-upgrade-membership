# Generated by Django 4.1.4 on 2023-07-18 04:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('masterapp', '0036_rename_chat_between_parties_membership_chat_between_parties'),
    ]

    operations = [
        migrations.RenameField(
            model_name='membership',
            old_name='chat_between_Parties',
            new_name='chat_between_parties',
        ),
    ]
