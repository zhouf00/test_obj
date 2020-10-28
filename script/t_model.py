# Django脚本化启动
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_obj.settings')
django.setup()

from engineering.models import Project, Manufacturer
from personnel import models
from rbac.models import Menu, Role, Auth

# user = models.User.objects.filter(pk=2)[0]
# print([var['title'] for var in user.roles.values()])
# print(Menu.objects.filter(user.roles.all()))

# if Project.objects.filter(sn=35):
#     print('该编号已经存在')

# print(Project.objects.filter(builders=2))
# print(models.User.objects.all())
# print(Auth.objects.filter(user__name='测试用户2').values())
# print(Menu.objects.filter(parent=None))
print(dict(models.Structure.objects.values_list('deptid', 'name')))
print(models.Structure.objects.values('user'))