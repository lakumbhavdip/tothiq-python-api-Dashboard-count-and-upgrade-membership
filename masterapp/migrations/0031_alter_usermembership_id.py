# Generated by Django 4.1.4 on 2023-07-17 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterapp', '0030_alter_usermembership_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermembership',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
