# Generated by Django 3.2.19 on 2023-08-29 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0071_alter_contracts_pin'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='folder_name_arabic',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
