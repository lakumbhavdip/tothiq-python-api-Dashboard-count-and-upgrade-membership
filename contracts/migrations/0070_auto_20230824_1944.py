# Generated by Django 3.2.19 on 2023-08-24 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0069_auto_20230823_1537'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categories',
            old_name='is_premium',
            new_name='business_Premium_Membership',
        ),
        migrations.AddField(
            model_name='categories',
            name='business_basic_Membership',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='categories',
            name='business_free_Membership',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='categories',
            name='category_name_arabic',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='categories',
            name='individual_Premium_Membership',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='categories',
            name='individual_basic_Membership',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='categories',
            name='individual_free_Membership',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='template',
            name='template_title_arabic',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='categories',
            name='category_availability',
            field=models.CharField(choices=[('Individual Membership', 'individual membership'), ('Business Membership', 'business membership')], default='', max_length=50),
        ),
    ]
