# Generated by Django 4.1.4 on 2023-06-24 06:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authtoken', '0003_tokenproxy'),
        ('business_admin', '0021_business_info_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomToken',
            fields=[
                ('token_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='authtoken.token')),
                ('business_id', models.IntegerField(blank=True, null=True)),
            ],
            bases=('authtoken.token',),
        ),
    ]
