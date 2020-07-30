from django.db import models
from django.contrib.auth.models import AbstractUser, Group

from utils.basemodel import BaseModel
# Create your models here.


class User(AbstractUser):

    GENDER_LIST = (
        (0, ''),
        (1, '男'),
        (2, '女')
    )

    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机')
    name = models.CharField(blank=True, max_length=32, verbose_name='中文名')
    gender = models.IntegerField(choices=GENDER_LIST, default=0, verbose_name='性别')
    avatar = models.URLField(blank=True,verbose_name='头像链接')
    main_department = models.IntegerField(default=0, verbose_name='主部门')

    department = models.ManyToManyField(
        to='Structure',
        # db_constraint=False,
        related_name='user',
        through='UserToStructure'
    )

    leader_dept = models.ManyToManyField(
        to='Structure',
        # db_constraint=False,
        related_name='leader',
        through='UserleaderToStructure'
    )

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
    TYPE_CHOICES = (
        ('firm', '公司'),
        ('department', '部门')
    )
    deptid = models.IntegerField(unique=True, verbose_name='部门ID')
    name = models.CharField(max_length=32, unique=True, verbose_name='部门名称')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='department', verbose_name='类型')
    parentid = models.ForeignKey('self', to_field='deptid', on_delete=models.CASCADE, null=True, blank=True, verbose_name='父类构架')
    order = models.IntegerField(verbose_name='排序')


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'departments'
        verbose_name = '部门表'
        verbose_name_plural = verbose_name


class UserToStructure(BaseModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False)
    structure = models.ForeignKey(Structure, to_field='deptid', on_delete=models.CASCADE, db_constraint=False)


class UserleaderToStructure(BaseModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False)
    structure = models.ForeignKey(Structure, to_field='deptid', on_delete=models.CASCADE ,db_constraint=False)
