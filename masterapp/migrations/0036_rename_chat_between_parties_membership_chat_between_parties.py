# Generated by Django 4.1.4 on 2023-07-18 04:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('masterapp', '0035_rename_add_free_premium_template_membership_free_premium_template_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='membership',
            old_name='Chat_between_Parties',
            new_name='chat_between_Parties',
        ),
    ]