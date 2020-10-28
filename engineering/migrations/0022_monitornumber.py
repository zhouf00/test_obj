# Generated by Django 2.2.6 on 2020-10-28 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('engineering', '0021_auto_20201026_2136'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonitorNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='监测类型名称')),
                ('number', models.SmallIntegerField(verbose_name='监测数量')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='number', to='engineering.Project')),
            ],
            options={
                'verbose_name': '监测类型数量',
                'verbose_name_plural': '监测类型数量',
            },
        ),
    ]