# Generated by Django 2.2.6 on 2020-11-16 14:15

from django.db import migrations, models
import django.db.models.deletion
import utils.basemodel


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EventLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('event_type', models.SmallIntegerField(default=1, verbose_name='事件类型')),
                ('detail', models.TextField(verbose_name='事件详情')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '日志',
                'verbose_name_plural': '日志',
            },
        ),
        migrations.CreateModel(
            name='IdcRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=32, verbose_name='设备名称')),
                ('sn', models.CharField(blank=True, max_length=64, null=True, verbose_name='SN号或快速服务代码')),
                ('describe', models.TextField(verbose_name='设备描述')),
                ('software', models.CharField(blank=True, max_length=32, null=True, verbose_name='安装软件版本')),
                ('ip', models.TextField(blank=True, null=True, verbose_name='ip信息')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '机房信息',
                'verbose_name_plural': '机房信息',
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=32, verbose_name='货物名称')),
                ('type', models.CharField(blank=True, max_length=32, null=True, verbose_name='发货类型')),
                ('count', models.IntegerField(blank=True, null=True, verbose_name='发货数量')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '发货清单',
                'verbose_name_plural': '发货清单',
            },
        ),
        migrations.CreateModel(
            name='InvoiceImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=64, null=True, verbose_name='文件名称')),
                ('image', models.ImageField(blank=True, null=True, upload_to=utils.basemodel.upload_path_image, verbose_name='图片')),
            ],
            options={
                'verbose_name': '发货图片',
                'verbose_name_plural': '发货图片',
            },
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=64, verbose_name='机器型号')),
                ('param', models.TextField(blank=True, null=True, verbose_name='设备参数')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '设备型号',
                'verbose_name_plural': '设备型号',
            },
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=64, verbose_name='厂商名称')),
                ('telephone', models.CharField(blank=True, max_length=11, null=True, verbose_name='厂商电话')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '厂商',
                'verbose_name_plural': '厂商',
            },
        ),
        migrations.CreateModel(
            name='MonitorNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='监测类型名称')),
                ('number', models.SmallIntegerField(verbose_name='监测数量')),
            ],
            options={
                'verbose_name': '监测类型数量',
                'verbose_name_plural': '监测类型数量',
            },
        ),
        migrations.CreateModel(
            name='MonitorType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='监测名称')),
            ],
            options={
                'verbose_name': '监测类型',
                'verbose_name_plural': '监测类型',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='项目名称')),
                ('priority', models.SmallIntegerField(default=1, verbose_name='优先级')),
                ('address', models.CharField(max_length=64, verbose_name='项目地址')),
                ('pj_sn', models.CharField(blank=True, max_length=64, null=True, verbose_name='项目编号')),
                ('sn', models.CharField(blank=True, max_length=64, null=True, verbose_name='内部编号')),
                ('facility_count', models.IntegerField(default=0, verbose_name='设备数量')),
                ('contractor', models.CharField(blank=True, max_length=64, null=True, verbose_name='承包商')),
                ('manager', models.CharField(blank=True, max_length=64, null=True, verbose_name='项目负责人')),
                ('province', models.CharField(blank=True, max_length=64, null=True, verbose_name='省份')),
                ('user_car', models.CharField(blank=True, max_length=64, null=True, verbose_name='项目负责人')),
                ('image', models.ImageField(blank=True, default='img/default.jpg', null=True, upload_to=utils.basemodel.upload_path_image, verbose_name='默认图片')),
                ('entrance_time', models.DateTimeField(blank=True, null=True, verbose_name='入场时间')),
                ('finish_time', models.DateTimeField(blank=True, null=True, verbose_name='完成时间')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注说明')),
            ],
            options={
                'verbose_name': '项目',
                'verbose_name_plural': '项目',
            },
        ),
        migrations.CreateModel(
            name='ProjectArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='区域名称')),
            ],
            options={
                'verbose_name': '区域信息',
                'verbose_name_plural': '区域信息',
            },
        ),
        migrations.CreateModel(
            name='ProjectStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='状态名称')),
            ],
            options={
                'verbose_name': '项目状态',
                'verbose_name_plural': '项目状态',
            },
        ),
        migrations.CreateModel(
            name='ProjectType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='项目类型')),
            ],
            options={
                'verbose_name': '项目类型',
                'verbose_name_plural': '项目类型',
            },
        ),
        migrations.CreateModel(
            name='ProjectWorkingEnv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='环境名称')),
            ],
            options={
                'verbose_name': '作业环境',
                'verbose_name_plural': '作业环境',
            },
        ),
        migrations.CreateModel(
            name='StockFinish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='标签')),
            ],
            options={
                'verbose_name': '库存完成与否',
                'verbose_name_plural': '库存完成与否',
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=32, verbose_name='货物名称')),
                ('totality', models.IntegerField(blank=True, null=True, verbose_name='货物总数')),
                ('delivered', models.IntegerField(blank=True, default=0, null=True, verbose_name='已发货')),
                ('undelivered', models.IntegerField(blank=True, default=0, null=True, verbose_name='未发货')),
                ('finish', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='engineering.StockFinish', verbose_name='是否完成')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stock', to='engineering.Project')),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='engineering.MonitorType', verbose_name='货物类型')),
            ],
            options={
                'verbose_name': '库存管理',
                'verbose_name_plural': '库存管理',
            },
        ),
        migrations.CreateModel(
            name='ProjectTrace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('content', models.TextField(verbose_name='内容')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trace', to='engineering.Project')),
            ],
            options={
                'verbose_name': '项目跟踪情况',
                'verbose_name_plural': '项目跟踪情况',
            },
        ),
    ]
