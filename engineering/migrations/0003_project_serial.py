# Generated by Django 2.2.6 on 2021-03-19 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engineering', '0002_auto_20210319_1820'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='serial',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='项目流水号'),
        ),
    ]
