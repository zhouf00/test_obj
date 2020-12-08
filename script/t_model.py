# Django脚本化启动
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_obj.settings')
django.setup()

from engineering.models import Project, Manufacturer
from personnel import models
from rbac.models import Menu, Auth
from product import models as product_models
from APPS.crm import models as crm_models

# user = models.User.objects.filter(pk=2)[0]
# print([var['title'] for var in user.roles.values()])
# print(Menu.objects.filter(user.roles.all()))

# print(len(Project.objects.filter(sn='0092'))==1)
# print(Project.objects.filter(manufacturers__id=3))

# print(Project.objects.filter(builders=2))
# print(models.User.objects.all())
# print(Auth.objects.filter(user__name='测试用户2').values())
# print(Menu.objects.filter(parent=None))
# print(dict(models.Structure.objects.values_list('deptid', 'name')))
# print(models.Structure.objects.values('user'))
# if len(product_models.Production.objects.filter(sn=1234)) == 0:
#     print('没有')

# 部门查询人
# print(models.Structure.objects.filter(depttouser=1))

##############
# 销售管理查询
##############
import datetime
# print(crm_models.Market.objects.filter(pk=8).first().hit_rate)
# print(crm_models.RateRecord.objects.filter(hit_rate=0.5).values())
# 时间计算
# start = crm_models.RateRecord.objects.filter(market=2).values()[0]['start_time']
# end = datetime.datetime.strptime('2020-12-1 15:30:20','%Y-%m-%d %H:%M:%S')
# print((end-start).days)
print(crm_models.Market.objects.filter(user__in=[15, 16, 17, 19]))
print(crm_models.Market.objects.filter(user__username__in=['ZhouWenXing', 'gen', 'ZhangJingJing', 'test1']))
# print(models.User.objects.filter())
# print(models.Structure.objects.filter(deptid__in=[3]).values('id'))
# print(models.DeptToUser.objects.filter(department=3))
# models.DeptToUser.objects.filter(department=3, user__in=['test1','ZhouWenXing']).update(isleader=True)
