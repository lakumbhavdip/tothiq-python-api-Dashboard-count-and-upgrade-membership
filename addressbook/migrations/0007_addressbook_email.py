# Generated by Django 4.1.4 on 2023-07-21 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addressbook', '0006_alter_addressbook_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='addressbook',
            name='email',
            field=models.CharField(max_length=100, null=True),
        ),
    ]