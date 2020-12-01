# Generated by Django 2.2.6 on 2020-11-27 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_auto_20201127_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='raterecord',
            name='days',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='天数'),
        ),
        migrations.AlterField(
            model_name='raterecord',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='结束时间'),
        ),
        migrations.AlterField(
            model_name='raterecord',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='开始时间'),
        ),
    ]
