# Generated by Django 3.2.19 on 2023-08-18 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0064_auto_20230817_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='description',
            field=models.TextField(),
        ),
    ]
