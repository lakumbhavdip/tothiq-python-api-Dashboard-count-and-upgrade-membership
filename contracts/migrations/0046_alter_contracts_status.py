# Generated by Django 4.1.4 on 2023-05-23 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0045_rename_contract_enddate_contracts_contract_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contracts',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('under_review', 'Under Review'), ('ready', 'Ready'), ('signed', 'Signed'), ('rejected', 'Rejected'), ('deleted', 'Deleted'), ('cancelled', 'Cancelled')], default='draft', max_length=15),
        ),
    ]
