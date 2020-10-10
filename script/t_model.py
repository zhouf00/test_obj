# Django脚本化启动
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_obj.settings')
django.setup()

from personnel import models
from rbac.models import Menu, Role

user = models.User.objects.filter(pk=2)[0]
print([var['title'] for var in user.roles.values()])
print(Menu.objects.filter(user.roles.all()))
# user.user_dept_set.


import random

