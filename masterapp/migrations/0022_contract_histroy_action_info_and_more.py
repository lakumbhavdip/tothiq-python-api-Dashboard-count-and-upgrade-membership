# Generated by Django 4.1.4 on 2023-07-14 05:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('masterapp', '0021_alter_usermembership_end_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract_histroy',
            name='action_info',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='contract_histroy',
            name='action_type',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='contract_histroy',
            name='contracts',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='contract_histroy',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='contract_histroy',
            name='parties',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='contract_histroy',
            name='users',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='usermembership',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='usermembership',
            name='net_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('payment_type', models.CharField(max_length=100)),
                ('contract_buy', models.IntegerField()),
                ('user_buy', models.IntegerField()),
                ('total_amount', models.DecimalField(decimal_places=3, max_digits=10)),
                ('discount_type', models.CharField(max_length=100)),
                ('discount_rate', models.DecimalField(decimal_places=3, max_digits=10)),
                ('discount_amount', models.DecimalField(decimal_places=3, max_digits=10)),
                ('net_amount', models.DecimalField(decimal_places=3, max_digits=10)),
                ('payment_method', models.CharField(max_length=100)),
                ('payment_status', models.CharField(max_length=100)),
                ('tr_id', models.CharField(max_length=100)),
                ('ref_number', models.CharField(max_length=100)),
                ('auth_code', models.CharField(max_length=100)),
                ('track_id', models.CharField(max_length=100)),
                ('payment_id', models.CharField(max_length=100)),
                ('payment_info', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('membership', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='masterapp.membership')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
