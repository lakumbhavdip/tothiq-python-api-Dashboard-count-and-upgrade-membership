# Generated by Django 3.2.19 on 2023-08-22 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business_admin', '0041_alter_business_info_authorized_signatory_expiry_date_and_more'),
        ('contracts', '0065_alter_template_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='contracts',
            name='business',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='business_admin.business_info'),
        ),
    ]