# Generated by Django 4.1.4 on 2023-05-16 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0023_template_authorised_person_template_company_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='template',
            old_name='days',
            new_name='day',
        ),
    ]
