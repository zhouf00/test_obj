# Generated by Django 2.2.6 on 2020-11-16 14:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('engineering', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='projecttrace',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trace', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project', to='engineering.ProjectArea', verbose_name='项目区域'),
        ),
        migrations.AddField(
            model_name='project',
            name='manufacturers',
            field=models.ManyToManyField(db_constraint=False, related_name='project', to='engineering.Manufacturer'),
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project', to='engineering.ProjectStatus', verbose_name='项目状态'),
        ),
        migrations.AddField(
            model_name='project',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project', to='engineering.ProjectType', verbose_name='项目类型'),
        ),
        migrations.AddField(
            model_name='project',
            name='working_env',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project', to='engineering.ProjectWorkingEnv', verbose_name='项目作业环境'),
        ),
        migrations.AddField(
            model_name='monitortype',
            name='project',
            field=models.ManyToManyField(blank=True, db_constraint=False, related_name='monitor_type', to='engineering.Project'),
        ),
        migrations.AddField(
            model_name='monitornumber',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='number', to='engineering.Project'),
        ),
        migrations.AddField(
            model_name='machine',
            name='manufacturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='machine', to='engineering.Manufacturer'),
        ),
        migrations.AddField(
            model_name='invoiceimage',
            name='invoice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='img', to='engineering.Invoice'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoice', to='engineering.Project'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='发货人'),
        ),
        migrations.AddField(
            model_name='idcroom',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='idcroom', to='engineering.Project'),
        ),
        migrations.AddField(
            model_name='eventlog',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='log', to='engineering.Project'),
        ),
    ]
