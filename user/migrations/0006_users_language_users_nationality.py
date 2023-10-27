# Generated by Django 4.1.4 on 2023-05-11 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masterapp', '0005_language'),
        ('user', '0005_remove_users_language_remove_users_nationality'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='language',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='masterapp.language'),
        ),
        migrations.AddField(
            model_name='users',
            name='nationality',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='masterapp.nationality_type'),
        ),
    ]
