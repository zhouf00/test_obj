# Generated by Django 2.2.6 on 2020-11-30 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
        ('crm', '0005_auto_20201127_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='market',
            name='amount',
            field=models.IntegerField(blank=True, null=True, verbose_name='漏额'),
        ),
        migrations.AddField(
            model_name='market',
            name='traceTime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='跟进时间'),
        ),
        migrations.AddField(
            model_name='market',
            name='type',
            field=models.ManyToManyField(db_constraint=False, related_name='market', to='product.Product'),
        ),
        migrations.AlterField(
            model_name='market',
            name='address',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='地区'),
        ),
        migrations.AlterField(
            model_name='market',
            name='company',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='集团公司'),
        ),
    ]
