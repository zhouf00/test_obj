# Generated by Django 2.2.6 on 2020-10-23 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('engineering', '0002_auto_20201023_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitortype',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monitor_type', to='engineering.Project'),
        ),
    ]
