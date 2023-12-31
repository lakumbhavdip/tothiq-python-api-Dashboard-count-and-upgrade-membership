# Generated by Django 4.1.4 on 2023-05-08 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0010_alter_notification_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='is_active',
        ),
        migrations.AddField(
            model_name='notification',
            name='read',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='notification',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='notification',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
