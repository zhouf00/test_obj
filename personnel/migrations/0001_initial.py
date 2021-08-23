# Generated by Django 2.2.6 on 2021-08-04 11:43

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('mobile', models.CharField(blank=True, max_length=11, null=True, verbose_name='手机')),
                ('name', models.CharField(blank=True, max_length=32, null=True, verbose_name='中文名')),
                ('gender', models.SmallIntegerField(default=1, verbose_name='性别')),
                ('avatar', models.URLField(default='https://ss0.baidu.com/94o3dSag_xI4khGko9WTAnF6hhy/zhidao/wh%3D450%2C600/sign=a300d7f4d958ccbf1be9bd3e2ce89008/c75c10385343fbf2a2cfd865b87eca8064388f90.jpg', verbose_name='头像链接')),
                ('main_department', models.IntegerField(default=0, verbose_name='主部门')),
                ('position', models.CharField(blank=True, max_length=32, null=True, verbose_name='岗位名称')),
            ],
            options={
                'verbose_name': '用户表',
                'verbose_name_plural': '用户表',
                'db_table': 'user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='DeptToUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isleader', models.BooleanField(default=False, verbose_name='是否领导')),
            ],
            options={
                'verbose_name': '用户部门中间表',
                'verbose_name_plural': '用户部门中间表',
                'db_table': 'user_departments',
            },
        ),
        migrations.CreateModel(
            name='Structure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('deptid', models.IntegerField(unique=True, verbose_name='部门ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='部门名称')),
                ('type', models.SmallIntegerField(default=0, verbose_name='类型')),
                ('order', models.IntegerField(blank=True, null=True, verbose_name='排序')),
            ],
            options={
                'verbose_name': '部门表',
                'verbose_name_plural': '部门表',
                'db_table': 'departments',
            },
        ),
    ]
