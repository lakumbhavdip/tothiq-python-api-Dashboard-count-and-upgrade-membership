# Generated by Django 4.1.4 on 2023-07-21 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addressbook', '0005_addressbook_active_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addressbook',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]