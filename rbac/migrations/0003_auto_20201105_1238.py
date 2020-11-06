# Generated by Django 2.2.6 on 2020-11-05 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0002_auto_20201105_1152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auth',
            name='menu',
        ),
        migrations.AddField(
            model_name='menu',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='menu', to='rbac.Auth'),
        ),
    ]
