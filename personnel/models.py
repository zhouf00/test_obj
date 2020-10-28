from django.db import models
from django.contrib.auth.models import AbstractUser

from utils.basemodel import BaseModel, upload_path_image
# Create your models here.


class User(AbstractUser):

    GENDER_LIST = (
        (0, ''),
        (1, '男'),
        (2, '女')
    )

    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机')
    name = models.CharField(blank=True, max_length=32, verbose_name='中文名')
    gender = models.SmallIntegerField(default=1, verbose_name='性别')
    avatar = models.URLField(default='https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1603364145011&di=010785ee75fa3669ca415d95ce401ce0&imgtype=0&src=http%3A%2F%2Fc-ssl.duitang.com%2Fuploads%2Fitem%2F201902%2F01%2F20190201234537_SEZMN.thumb.400_0.jpeg',
                             verbose_name='头像链接')
    main_department = models.IntegerField(default=0, verbose_name='主部门')

    department = models.ManyToManyField(
        to='Structure',
        related_name='user',
        through='DeptToUser',
        through_fields=('user', 'department')
    )

    project = models.ForeignKey(
        to='engineering.Project',
        on_delete=models.CASCADE,
        related_name='builders',
        blank=True, null=True
    )

    @property
    def info(self):
        return {
            'id': self.id,
            'name': self.name
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
    parentid = models.ForeignKey('self', to_field='deptid', on_delete=models.CASCADE, null=True, blank=True, verbose_name='父类构架')
    order = models.IntegerField(verbose_name='排序')

    menu = models.ManyToManyField(
        to='rbac.Menu',
        db_constraint=False,
        related_name='department',
    )

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
