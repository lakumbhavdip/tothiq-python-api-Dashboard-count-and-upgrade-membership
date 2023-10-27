# Generated by Django 4.1.4 on 2023-05-29 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0049_contracts_appendix'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contracts',
            name='contract_end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='contracts',
            name='contract_start_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='contracts',
            name='contract_title',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='contracts',
            name='contract_valuation',
            field=models.DecimalField(decimal_places=3, max_digits=500, null=True),
        ),
        migrations.AlterField(
            model_name='contracts',
            name='description',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
