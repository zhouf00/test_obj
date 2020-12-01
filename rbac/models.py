from django.db import models

from utils.basemodel import BaseModel
# Create your models here.

class Menu(BaseModel):
    """
    菜单：页面路径
    """
    title = models.CharField(max_length=32, unique=True, verbose_name='菜单名')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='父菜单',
                               related_name='children')
    icon = models.CharField(max_length=50, null=True, blank=True, verbose_name='图标')
    url = models.CharField(max_length=128, null=True, blank=True, verbose_name='路径')
    name = models.CharField(max_length=64, null=True, blank=True, verbose_name='前端名称')

    role = models.ForeignKey(
        to='Auth',
        on_delete=models.CASCADE,
        related_name='menu',
        blank=True, null=True
    )

    @property
    def parentInfo(self):
        return {
            'title':self.parent.title
        }
    @property
    def childrenList(self):
        return self.children.values('id', 'title')

    def __str__(self):
        title_list = [self.title]
        p = self.parent
        while p:
            title_list.insert(0, p.title)
            p = p.parent
        return '-'.join(title_list)

    class Meta:
        verbose_name = '菜单'
        verbose_name_plural = verbose_name


class Auth(models.Model):

    title = models.CharField(max_length=32, verbose_name='管理员角色')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')

    user = models.ManyToManyField(
        to='personnel.User',
        db_constraint=False,
        related_name='auth',
    )

    @property
    def userList(self):
        return self.user.values('id', 'name')

    @property
    def menuList(self):
        return self.menu.values('id', 'title')

    class Meta:
        verbose_name = '权限表'
        verbose_name_plural = verbose_name
