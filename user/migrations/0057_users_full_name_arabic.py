# Generated by Django 3.2.19 on 2023-09-07 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0056_users_signature_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='full_name_arabic',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
