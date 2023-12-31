# Generated by Django 4.1.4 on 2023-05-18 10:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contracts', '0028_contracts_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='contracts',
            name='status',
            field=models.CharField(default='draft', max_length=15),
        ),
        migrations.AddField(
            model_name='contracts',
            name='template',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contracts.template'),
        ),
        migrations.CreateModel(
            name='contract_party',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('civil_id', models.CharField(max_length=12)),
                ('email', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.contracts')),
                ('user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'contracts_party',
            },
        ),
    ]
