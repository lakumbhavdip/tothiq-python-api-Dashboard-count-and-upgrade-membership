# Generated by Django 4.1.4 on 2023-07-28 06:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('addressbook', '0008_addressbook_full_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addressbook',
            name='full_name',
        ),
    ]
