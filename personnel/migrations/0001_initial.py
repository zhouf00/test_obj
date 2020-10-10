# Generated by Django 2.2.6 on 2020-08-15 09:40

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Structure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=1)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('deptid', models.IntegerField(unique=True, verbose_name='部门ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='部门名称')),
                ('type', models.CharField(choices=[('firm', '公司'), ('department', '部门')], default='department', max_length=20, verbose_name='类型')),
                ('order', models.IntegerField(verbose_name='排序')),
                ('parentid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='personnel.Structure', to_field='deptid', verbose_name='父类构架')),
            ],
            options={
                'verbose_name': '部门表',
                'verbose_name_plural': '部门表',
                'db_table': 'departments',
            },
        ),
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
                ('mobile', models.CharField(max_length=11, unique=True, verbose_name='手机')),
                ('name', models.CharField(blank=True, max_length=32, verbose_name='中文名')),
                ('gender', models.IntegerField(choices=[(0, ''), (1, '男'), (2, '女')], default=0, verbose_name='性别')),
                ('avatar', models.URLField(blank=True, verbose_name='头像链接')),
                ('main_department', models.IntegerField(default=0, verbose_name='主部门')),
                ('department', models.ManyToManyField(db_constraint=False, related_name='user', to='personnel.Structure')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('leader_dept', models.ManyToManyField(db_constraint=False, related_name='leader', to='personnel.Structure')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
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
    ]
