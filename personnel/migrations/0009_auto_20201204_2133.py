# Generated by Django 2.2.6 on 2020-12-04 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personnel', '0008_auto_20201204_1800'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='depttouser',
            options={'verbose_name': '用户部门中间表', 'verbose_name_plural': '用户部门中间表'},
        ),
        migrations.AlterField(
            model_name='depttouser',
            name='isleader',
            field=models.BooleanField(default=False, verbose_name='是否领导'),
        ),
        migrations.AlterField(
            model_name='user',
            name='department',
            field=models.ManyToManyField(related_name='users', through='personnel.DeptToUser', to='personnel.Structure'),
        ),
        migrations.AlterModelTable(
            name='depttouser',
            table='user_department',
        ),
    ]