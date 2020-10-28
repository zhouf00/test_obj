# Generated by Django 2.2.6 on 2020-10-23 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('engineering', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='monitor_type',
        ),
        migrations.AddField(
            model_name='monitortype',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='monitor_type', to='engineering.MonitorType'),
            preserve_default=False,
        ),
    ]