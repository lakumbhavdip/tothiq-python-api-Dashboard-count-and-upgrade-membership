# Generated by Django 4.1.4 on 2023-07-17 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterapp', '0033_rename_edit_templates_membership_add_free_premium_template_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='membership_amount',
            field=models.DecimalField(decimal_places=3, max_digits=10, null=True),
        ),
    ]