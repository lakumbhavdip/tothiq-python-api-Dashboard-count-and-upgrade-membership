# Generated by Django 4.1.4 on 2023-07-25 07:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('masterapp', '0046_alter_usermembership_payment_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('payment_name', models.CharField(max_length=500, null=True)),
                ('payment_status', models.BooleanField(null=True)),
                ('payment_transportal_id', models.CharField(max_length=500, null=True)),
                ('payment_transportal_password', models.CharField(max_length=500, null=True)),
                ('payment_terminal_resource_key', models.CharField(max_length=500, null=True)),
                ('payment_test_mode', models.BooleanField(null=True)),
            ],
            options={
                'db_table': 'paymentmethod',
            },
        ),
        migrations.AddField(
            model_name='membership',
            name='collaborative_editing',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='membership',
            name='number_of_user',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='membership',
            name='revision_history',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='membership',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
