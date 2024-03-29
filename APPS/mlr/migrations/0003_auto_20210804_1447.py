# Generated by Django 2.2.6 on 2021-08-04 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mlr', '0002_auto_20210804_1143'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecialEnv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='特殊工作环境')),
            ],
            options={
                'verbose_name': '特殊工作环境',
                'verbose_name_plural': '特殊工作环境',
            },
        ),
        migrations.AlterModelOptions(
            name='otherenv',
            options={'verbose_name': '工作环境', 'verbose_name_plural': '工作环境'},
        ),
        migrations.AddField(
            model_name='worklogs',
            name='special_env',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='关联-(SpecialEnv) 特殊环境'),
        ),
        migrations.AlterField(
            model_name='otherenv',
            name='title',
            field=models.CharField(max_length=64, verbose_name='工作环境'),
        ),
        migrations.AlterField(
            model_name='worklogs',
            name='other_env',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='关联-(OtherEnv) 工作环境'),
        ),
    ]
