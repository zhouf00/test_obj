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
        related_name='user',
        through='DeptToUser',
        through_fields=('user', 'department')
    )

    departments = models.ManyToManyField(
        to='Structure',
        related_name='users',
        db_constraint=False,
    )

    dept_leader = models.ManyToManyField(
        to='Structure',
        related_name='leader',
        db_constraint=False,
    )

    project = models.ForeignKey(
        to='engineering.Project',
        on_delete=models.CASCADE,
        related_name='builders',
        blank=True, null=True
    )

    @property
    def menus(self):
        list = self.auth.values('menu__name')
        # print(list)
        menu = [ var['menu__name'] for var in list if var['menu__name'] ]
        return menu

    @property
    def roleList(self):
        list = self.auth.values('id', 'title')
        role = [ var['title'] for var in list ]
        return role

    @property
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
    leader = models.BooleanField(verbose_name='是否领导')
