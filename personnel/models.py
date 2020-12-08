# _*_ coding: utf-8 _*_
from django.db import models
from django.contrib.auth.models import AbstractUser

from utils.basemodel import BaseModel, upload_path_image
# Create your models here.


class User(AbstractUser):

    mobile = models.CharField(max_length=11, blank=True, null=True, verbose_name='手机')
    name = models.CharField(blank=True, null=True, max_length=32, verbose_name='中文名')
    gender = models.SmallIntegerField(default=1, verbose_name='性别')
    avatar = models.URLField(default='https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=2866953378,474015488&fm=11&gp=0.jpg',
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
            if var['menu__name'] not in menu:
                menu.append(var['menu__name'])
        return menu

    @property   # 获取管理员身份
    def roleList(self):
        list = self.auth.values('id', 'title')
        role = [var['title'] for var in list ]
        return role

    @property   # 获取管理的部门
    def deptList(self):
        d = self.depttouser_set.values()
        leaders = [var['department_id']for var in d if var['isleader']]
        # print('管理的部门ID:',leaders)
        return leaders

    @property   # 获取管理部门的成员
    def deptmembers(self):
        d_list = []
        d = self.department.filter(deptid__in=self.deptList)
        for var in d:
            d_list += list(var.depttouser_set.values('user_id'))
        users = [var['user_id'] for var in d_list]
        # print('部门成员的ID:', users)
        return users

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
