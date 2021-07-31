# _*_ coding: utf-8 _*_
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

from utils.basemodel import BaseModel, upload_path_image
# Create your models here.


class User(AbstractUser):

    mobile = models.CharField(max_length=11, blank=True, null=True, verbose_name='手机')
    name = models.CharField(blank=True, null=True, max_length=32, verbose_name='中文名')
    gender = models.SmallIntegerField(default=1, verbose_name='性别')
    avatar = models.URLField(default='https://ss0.baidu.com/94o3dSag_xI4khGko9WTAnF6hhy/zhidao/wh%3D450%2C600/sign=a300d7f4d958ccbf1be9bd3e2ce89008/c75c10385343fbf2a2cfd865b87eca8064388f90.jpg',
                             verbose_name='头像链接')
    main_department = models.IntegerField(default=0, verbose_name='主部门')
    position = models.CharField(max_length=32, blank=True, null=True, verbose_name='岗位名称')

    department = models.ManyToManyField(
        to='Structure',
        related_name='users',
        through='DeptToUser',
        through_fields=('user', 'department'),
        default=[1]
    )

    project = models.ForeignKey(
        to='engineering.Project',
        on_delete=models.CASCADE,
        related_name='builders',
        blank=True, null=True
    )

    @property   # 获取有权限的菜单
    def menus(self):
        menu_list = list(self.auth.values('menu__name'))
        # print(menu_list)
        menu_list+=list(self.department.values('menu__name'))
        # print(list)
        # menu = [ var['menu__name'] for var in menu_list if var['menu__name'] ]
        menu = []
        for var in menu_list:
            if var['menu__name'] not in menu and var['menu__name']:
                menu.append(var['menu__name'])
        # print(menu)
        return menu

    @property   # 获取管理员身份
    def roleList(self):
        list = self.auth.values('id', 'title')
        role = [var['title'] for var in list ]
        return role

    @property   # 获取管理的部门
    def deptList(self):
        d = self.depttouser_set.values()
        dept_list = [var['department_id']for var in d if var['isleader']]
        child_list = []
        # 只可以获取2层子部门
        if dept_list:
            child_d = self.department.filter(deptid__in=dept_list).exclude(children__deptid=None).values('children__deptid', 'children__children__deptid')
            # print(child_d)
            for var in child_d:
                if var['children__deptid'] and not var['children__children__deptid']:
                    if not child_list.count(var['children__deptid']):
                        child_list.append(var['children__deptid'])
                else:
                    # if not child_list.count(var['children__deptid']):
                    #     child_list.append(var['children__deptid'])
                    if not child_list.count(var['children__children__deptid']):
                        child_list.append(var['children__children__deptid'])
        # print('管理的部门ID:',dept_list,child_list)
        return dept_list+child_list

    @property   # 获取管理部门的成员
    def deptmembers(self):
        d_list = []
        # d = self.department.filter(deptid__in=self.deptList)
        d = Structure.objects.filter(deptid__in=self.deptList)
        for var in d:
            d_list += list(var.depttouser_set.values('user', 'user__name', 'user__id'))
        # print(d_list)
        users = [var['user'] for var in d_list]
        users_name = [var['user__name'] for var in d_list]
        users_id = [var['user__id'] for var in d_list]
        # print('部门成员的ID:', users, users_name)
        # 0 返回username ; 0 返回name
        return users,users_name, users_id

    @property
    def markethistoryInfo(self):
        d = self.markethistory.filter(date__year=datetime.now().strftime('%Y')).values().order_by('date')
        d_dict = {var['date'].strftime('%m')+'月': var for var in d}
        if d_dict:
            return d_dict
        else:
            return {}

    @property   # 以字典的形式发送用户的指定信息
    def info(self):
        return {
            'id': self.id,
            'name': self.name,
            'username':self.username,
            'avatar': self.avatar
        }

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name


class Structure(BaseModel):
    """
    组织构架
    """
    deptid = models.IntegerField(unique=True, verbose_name='部门ID')
    name = models.CharField(max_length=32, unique=True, verbose_name='部门名称')
    type = models.SmallIntegerField(default=0, verbose_name='类型')
    parentid = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='父类构架',
                                  to_field='deptid', related_name='children')
    order = models.IntegerField(blank=True, null=True, verbose_name='排序')

    menu = models.ManyToManyField(
        to='rbac.Menu',
        db_constraint=False,
        related_name='department',
    )

    @property
    def usersInfoList(self):
        users = self.depttouser_set.values('user_id', 'user__name', 'isleader')
        user_list = [{'username': var['user_id'], 'name': var['user__name']} for var in users]
        return user_list

    @property
    def userList(self):
        users = self.depttouser_set.values('user_id')
        user_list = [var['user_id'] for var in users]
        return user_list

    @property
    def leaders(self):
        users = self.depttouser_set.values('user_id', 'user__name','isleader')
        # print(users)
        leader_list = [{'username': var['user_id'], 'name': var['user__name']}for var in users if var['isleader']]
        return leader_list

    @property
    def leaderList(self):
        users = self.depttouser_set.values('user_id', 'isleader')
        user_list = [var['user_id'] for var in users if var['isleader']]
        return user_list

    @property
    def childrenList(self):
        return self.children.values('id','name')


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'departments'
        verbose_name = '部门表'
        verbose_name_plural = verbose_name


class DeptToUser(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')
    department = models.ForeignKey(Structure, on_delete=models.CASCADE, to_field='deptid')
    isleader = models.BooleanField(default=False, verbose_name='是否领导')

    class Meta:
        db_table = 'user_departments'
        verbose_name = '用户部门中间表'
        verbose_name_plural = verbose_name
