import xadmin
from xadmin.plugins.auth import UserAdmin
from . import models

class MyUserAdmin(UserAdmin):
    list_display = ['username', 'mobile', 'name', 'gender', 'main_department', 'department',]
    list_filter = ['is_superuser', 'is_active']


class StructureAdmin(object):
    list_display = ['name', 'type', 'parentid', 'order', 'deptid']
    list_filter = []

xadmin.site.unregister(models.User)
xadmin.site.register(models.User, MyUserAdmin)
xadmin.site.register(models.Structure, StructureAdmin)