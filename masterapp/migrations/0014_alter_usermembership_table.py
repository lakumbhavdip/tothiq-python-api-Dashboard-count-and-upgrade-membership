# Generated by Django 4.1.4 on 2023-06-02 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('masterapp', '0013_usermembership'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='usermembership',
            table='user_membership',
        ),
    ]
