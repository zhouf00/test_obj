# Generated by Django 2.2.6 on 2020-07-24 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engineering', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='entrance_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='入场时间'),
        ),
        migrations.AlterField(
            model_name='project',
            name='finish_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='完成时间'),
        ),
        migrations.AlterField(
            model_name='project',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='默认图片'),
        ),
    ]
