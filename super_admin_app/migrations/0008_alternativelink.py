# Generated by Django 3.2.19 on 2023-09-27 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('super_admin_app', '0007_email_template_email_content_arabic'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlternativeLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_url', models.URLField(unique=True)),
                ('alternative_url', models.URLField(blank=True, null=True, unique=True)),
                ('created_date', models.DateTimeField(null=True)),
                ('updated_date', models.DateTimeField(null=True)),
                ('expire_date', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'alternativelink',
            },
        ),
    ]