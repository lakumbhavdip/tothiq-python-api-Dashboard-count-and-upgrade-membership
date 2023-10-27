# Generated by Django 3.2.19 on 2023-09-07 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masterapp', '0064_rename_country_currency_countrycurrency'),
        ('contracts', '0073_template_description_arabic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contracts',
            old_name='contract_valuation',
            new_name='contract_amount',
        ),
        migrations.AddField(
            model_name='contracts',
            name='contract_amount_words',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='contracts',
            name='contract_duration',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='contracts',
            name='contract_fees',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='contracts',
            name='currency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='masterapp.countrycurrency'),
        ),
    ]
