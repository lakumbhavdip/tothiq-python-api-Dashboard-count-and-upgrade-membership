# Generated by Django 4.1.4 on 2023-05-10 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterapp', '0002_nationality_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='address_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'address_type',
            },
        ),
    ]
