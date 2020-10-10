from django.db import models

from utils.basemodel import BaseModel
# Create your models here.

class Menu(BaseModel):
    """
    菜单：页面路径
    """
    title = models.CharField(max_length=32, unique=True, verbose_name='菜单名')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='父菜单')
    icon = models.CharField(max_length=50, null=True, blank=True, verbose_name='图标')
    url = models.CharField(max_length=128, unique=True, null=True, blank=True, verbose_name='路径')

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

class Role(BaseModel):
    """
    角色：绑定权限
    """
    title = models.CharField(max_length=32, verbose_name='角色名称')
    permissions = models.ManyToManyField('Menu', blank=True)

    @property
    def count(self):
        return len(self.user.values())

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = verbose_name