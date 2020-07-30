# Django脚本化启动
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_obj.settings')
django.setup()

from personnel import models

user = models.User.objects.filter(pk=1)[0]
print(user.departments.all())
print(user.user_dept_set.filter(isleader=0))
print(user.is_leader_in_dept.all())
print(user.dept)
# user.user_dept_set.
