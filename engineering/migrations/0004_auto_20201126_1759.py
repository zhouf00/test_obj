# Generated by Django 2.2.6 on 2020-11-26 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engineering', '0003_auto_20201124_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outsourcer',
            name='title',
            field=models.CharField(default=1, max_length=64, verbose_name='承包商名称'),
            preserve_default=False,
        ),
    ]