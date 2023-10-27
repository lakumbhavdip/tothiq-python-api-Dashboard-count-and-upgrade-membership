# Generated by Django 4.1.4 on 2023-05-22 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0042_contracts_folder'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contract_party',
            old_name='civil_id',
            new_name='second_party_civil_id',
        ),
        migrations.RemoveField(
            model_name='contract_party',
            name='email',
        ),
        migrations.RemoveField(
            model_name='contract_party',
            name='name',
        ),
        migrations.AddField(
            model_name='contract_party',
            name='first_party_email',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='contract_party',
            name='first_party_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='contract_party',
            name='second_party_email',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='contract_party',
            name='second_party_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='contracts',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('under-review', 'Under Review'), ('ready', 'Ready'), ('signed', 'Signed'), ('rejected', 'Rejected'), ('deleted', 'Deleted'), ('cancelled', 'Cancelled')], default='draft', max_length=15),
        ),
    ]
