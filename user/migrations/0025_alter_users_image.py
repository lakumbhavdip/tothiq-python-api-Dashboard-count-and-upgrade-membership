# Generated by Django 4.1.4 on 2023-05-31 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0024_alter_users_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='tothiq_pic'),
        ),
    ]
