# Generated by Django 3.2.19 on 2023-10-16 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterapp', '0071_alter_coupon_selected_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalsettings',
            name='paci_expire_time',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='generalsettings',
            name='paci_recall_time',
            field=models.IntegerField(null=True),
        ),
    ]
