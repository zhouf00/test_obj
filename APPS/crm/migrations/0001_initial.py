# Generated by Django 2.2.6 on 2020-11-26 17:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=64, verbose_name='商机名称')),
                ('customer', models.CharField(blank=True, max_length=64, null=True, verbose_name='客户名称')),
                ('company', models.CharField(blank=True, max_length=64, null=True, verbose_name='客户公司')),
                ('address', models.CharField(max_length=128, verbose_name='地址')),
                ('designing_institute', models.CharField(blank=True, max_length=64, null=True, verbose_name='设计院')),
                ('manufacturer', models.CharField(blank=True, max_length=64, null=True, verbose_name='制造厂')),
                ('sn', models.CharField(blank=True, max_length=32, null=True, verbose_name='编号')),
                ('count', models.IntegerField(blank=True, null=True, verbose_name='设置数量')),
                ('estimated_time', models.DateTimeField(blank=True, null=True, verbose_name='预计时间')),
                ('estimated_amount', models.IntegerField(blank=True, null=True, verbose_name='预额')),
                ('hit_rate', models.FloatField(blank=True, null=True, verbose_name='命中率')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '商机信息表',
                'verbose_name_plural': '商机信息表',
            },
        ),
        migrations.CreateModel(
            name='RateRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(verbose_name='开始时间')),
                ('end_time', models.DateTimeField(verbose_name='结束时间')),
                ('hit_rate', models.FloatField(verbose_name='命中率')),
            ],
            options={
                'verbose_name': '命中率过程记录',
                'verbose_name_plural': '命中率过程记录',
            },
        ),
        migrations.CreateModel(
            name='MarketTrace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('hit_rate', models.FloatField(verbose_name='命中率')),
                ('content', models.TextField(verbose_name='内容')),
                ('market', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='markettrace', to='crm.Market')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='markettrace', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '商机跟踪情况',
                'verbose_name_plural': '商机跟踪情况',
            },
        ),
        migrations.AddField(
            model_name='market',
            name='r1',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r1', to='crm.RateRecord', verbose_name='命中率 0'),
        ),
        migrations.AddField(
            model_name='market',
            name='r2',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r2', to='crm.RateRecord', verbose_name='命中率 25%'),
        ),
        migrations.AddField(
            model_name='market',
            name='r3',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r3', to='crm.RateRecord', verbose_name='命中率 50%'),
        ),
        migrations.AddField(
            model_name='market',
            name='r4',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r4', to='crm.RateRecord', verbose_name='命中率 75%'),
        ),
        migrations.AddField(
            model_name='market',
            name='user',
            field=models.ManyToManyField(db_constraint=False, related_name='market', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Linkman',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=32, verbose_name='联系人名字')),
                ('identity', models.CharField(blank=True, max_length=32, null=True, verbose_name='身份')),
                ('duty', models.CharField(blank=True, max_length=32, null=True, verbose_name='职务')),
                ('phone', models.CharField(blank=True, max_length=11, null=True, verbose_name='手机')),
                ('wechat', models.CharField(blank=True, max_length=64, null=True, verbose_name='微信')),
                ('mail', models.EmailField(blank=True, max_length=254, null=True, verbose_name='邮箱')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('market', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='linkman', to='crm.Market')),
            ],
            options={
                'verbose_name': '商机联系人',
                'verbose_name_plural': '商机联系人',
            },
        ),
    ]
