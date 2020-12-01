# Generated by Django 2.2.6 on 2020-12-01 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_auto_20201130_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='market',
            name='amount',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='漏额'),
        ),
        migrations.AlterField(
            model_name='market',
            name='estimated_amount',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='预额'),
        ),
        migrations.AlterField(
            model_name='market',
            name='hit_rate',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='命中率'),
        ),
    ]
