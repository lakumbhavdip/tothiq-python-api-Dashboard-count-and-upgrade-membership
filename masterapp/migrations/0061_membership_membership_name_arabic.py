# Generated by Django 3.2.19 on 2023-09-06 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterapp', '0060_auto_20230906_1041'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='membership_name_arabic',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
