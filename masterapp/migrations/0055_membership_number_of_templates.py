# Generated by Django 3.2.19 on 2023-08-31 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterapp', '0054_activity_logs'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='number_of_templates',
            field=models.IntegerField(null=True),
        ),
    ]
