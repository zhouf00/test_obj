# Generated by Django 2.2.6 on 2021-03-10 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
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
            ],
            options={
                'verbose_name': '商机联系人',
                'verbose_name_plural': '商机联系人',
            },
        ),
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=64, verbose_name='商机名称')),
                ('customer', models.CharField(blank=True, max_length=64, null=True, verbose_name='客户名称')),
                ('company', models.CharField(blank=True, max_length=64, null=True, verbose_name='集团公司')),
                ('address', models.CharField(blank=True, max_length=128, null=True, verbose_name='地区')),
                ('designing_institute', models.CharField(blank=True, max_length=64, null=True, verbose_name='设计院')),
                ('manufacturer', models.CharField(blank=True, max_length=64, null=True, verbose_name='制造厂')),
                ('sn', models.CharField(blank=True, max_length=32, null=True, verbose_name='编号')),
                ('count', models.IntegerField(blank=True, null=True, verbose_name='设置数量')),
                ('estimated_time', models.DateTimeField(blank=True, null=True, verbose_name='预计时间')),
                ('estimated_amount', models.FloatField(blank=True, default=0, null=True, verbose_name='预额')),
                ('hit_rate', models.FloatField(blank=True, default=0, null=True, verbose_name='命中率')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('traceTime', models.DateTimeField(blank=True, null=True, verbose_name='跟进时间')),
                ('amount', models.FloatField(blank=True, default=0, null=True, verbose_name='漏额')),
            ],
            options={
                'verbose_name': '商机信息表',
                'verbose_name_plural': '商机信息表',
            },
        ),
        migrations.CreateModel(
            name='MarketHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estimated_amount', models.FloatField(blank=True, default=0, null=True, verbose_name='预额')),
                ('amount', models.FloatField(blank=True, default=0, null=True, verbose_name='漏额')),
                ('rate_0', models.FloatField(blank=True, default=0, null=True, verbose_name='0%预额')),
                ('rate_0_t', models.SmallIntegerField(blank=True, default=0, null=True, verbose_name='0%个数')),
                ('rate_025', models.FloatField(blank=True, default=0, null=True, verbose_name='25%预额')),
                ('rate_025_t', models.SmallIntegerField(blank=True, default=0, null=True, verbose_name='25%个数')),
                ('rate_050', models.FloatField(blank=True, default=0, null=True, verbose_name='50%预额')),
                ('rate_050_t', models.SmallIntegerField(blank=True, default=0, null=True, verbose_name='50%个数')),
                ('rate_075', models.FloatField(blank=True, default=0, null=True, verbose_name='75%预额')),
                ('rate_075_t', models.SmallIntegerField(blank=True, default=0, null=True, verbose_name='75%个数')),
                ('rate_100', models.FloatField(blank=True, default=0, null=True, verbose_name='100%预额')),
                ('rate_100_t', models.SmallIntegerField(blank=True, default=0, null=True, verbose_name='100%个数')),
                ('date', models.DateTimeField(blank=True, null=True, verbose_name='日期')),
            ],
            options={
                'verbose_name': '月历史记录',
                'verbose_name_plural': '月历史记录',
            },
        ),
        migrations.CreateModel(
            name='RateRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(blank=True, null=True, verbose_name='开始时间')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='结束时间')),
                ('hit_rate', models.FloatField(verbose_name='命中率')),
                ('days', models.SmallIntegerField(blank=True, default=0, null=True, verbose_name='天数')),
                ('market', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='record', to='crm.Market', verbose_name='命中率记录')),
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
            ],
            options={
                'verbose_name': '商机跟踪情况',
                'verbose_name_plural': '商机跟踪情况',
            },
        ),
    ]
