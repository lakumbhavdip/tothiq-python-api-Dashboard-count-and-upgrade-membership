# Generated by Django 3.2.19 on 2023-09-26 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0071_auto_20230926_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='last_login',
            field=models.DateTimeField(null=True),
        ),
    ]
