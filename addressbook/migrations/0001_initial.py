# Generated by Django 4.1.4 on 2023-05-01 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Addressbook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('civil_id', models.CharField(max_length=12)),
            ],
            options={
                'db_table': 'addressbook',
            },
        ),
    ]
